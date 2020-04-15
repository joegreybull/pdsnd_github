import time
import datetime
import pandas as pd
import numpy as np
import string

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:25:06 2020

@author: Owner

Sources used as reference: https://pandas.pydata.org/, StackOverflow, https://thispointer.com/
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

Cities = ['chicago', 'new york city', 'washington']
Months = ['all','january', 'february', 'march', 'april', 'may', 'june']
Days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','Sunday']

def input_prompt(prompt, prompt_list):
    print("Enter the " + prompt)
    for i in range(0,len(prompt_list)):
        print(str(i) + " - " + prompt_list[i])
    
    while True:
        choice = input("Your Choice: ")
        try:
            if int(choice) >= 0 and int(choice) < len(prompt_list):
                break
        except Exception as e:
            print("Invalid, try again!")
            continue

    return choice


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_value = input_prompt('City', Cities)
    city = Cities[int(city_value)]
 
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input_prompt('Month', Months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_prompt('Day of Week', Days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # TO DO: load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = df['Start Time'].astype('datetime64[ns]')
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['dayoweek'] = df['Start Time'].dt.weekday_name

    if month == 0 and day == 0:
        return df
    elif month != 0 and day == 0:
        return df[(df.month == month)]
    elif month == 0 and day != 0: 
        return df[(df.day == day - 1)]
    elif month != 0 and day != 0:
        return df[(df.month == int(month)) & (df.day == day - 1)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = df['Start Time'].astype('datetime64[ns]')

    # TO DO: display the most common month
    try:
        most_common_month = df['month'].mode()[0]
        print("Most Common Month = " + string.capwords(Months[most_common_month]))
    except Exception as e:
        print("Most Common Month not available!")

    # TO DO: display the most common day of week
    try:
        most_common_weekday = df['dayoweek'].mode()[0]
        print("Most Common Weekday = " + most_common_weekday)
    except Exception as e:
        print("Most Common Weekday not available!")
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("Most Common Hour = " + str(most_common_hour))
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print("Most Common Start Station = " + most_common_start)

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print("Most Common End Station = " + most_common_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Combined Stations'] = df['Start Station'] + " to " + df['End Station']
    most_common_route = df['Combined Stations'].mode()[0]
    print("Most Common Route = " + most_common_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    total_trip_time = str(datetime.timedelta(seconds=int(total_trip_duration)))

    print("Total Trip Time = " + total_trip_time)

    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    mean_trip_time = str(datetime.timedelta(seconds=int(mean_trip_duration)))
    print("Mean Trip Time = " + mean_trip_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df.groupby(['User Type'])['User Type'].count())

    # TO DO: Display counts of gender
    print()
    try:
        print(df.groupby(['Gender'])['Gender'].count())
    except Exception as e:
        print("Gender: This statistic is unavailable")

    # TO DO: Display earliest, most recent, and most common year of birth
    print()
    try:
        earliest_birthday = str(int(df['Birth Year'].min()))
        print("Earliest Birth Date = " + earliest_birthday)

        print()
        recent_birthday = str(int(df['Birth Year'].max()))
        print("Most Recent Birth Date = " + recent_birthday)
    
        print()
        common_birthday = df['Birth Year'].mode()[0]
        print("Most Common Birth Date = " + str(int(common_birthday)))
        
    except Exception as e:
        print("Birth Date Statistics not available!")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_top_n(data, rows):
    print(data.head(rows))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, int(month), int(day))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_top_n(df, 5)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
