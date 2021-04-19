import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ["all", "january", "february", "march", "april", "may", "june"]
days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter a city you are interested in: ').strip().lower()
        if city not in CITY_DATA:
            print("Oops - you entered a city which is not listed!")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter a month you are interested in: ').strip().lower()
        if month not in months:
            print('It seems you entered a month where no data exists!')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter a day of the week you are interested in: ').strip().lower()
        if day not in days:
            print('Oops - It seems you didn´t entered a day!')
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # checking dimension, shape, size and type of the data frame
    print(df)
    print("\n Here you get some Information regarding your Data Set.\n")
    print(df.shape)
    print(type(df))
    print(df.ndim)
    print(df.size)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.day_name()
    # added new column "hour" for the function time_stats
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day.title()]
    return df

def output_snips_of_data(df):
    """Extends the Output Data Set by user Input.
        Args:
            (DataFrame) df - Pandas DataFrame with city data filtered by month and day
        """
    print(df.head(5))
    extend_data_set = input("Do you want to see more rows of the Data set? \n").strip().lower()

    """The User gets the first 5 rows. But if he wants to see more Data, he get asked. By Pressing yes the while-loop 
    will continue and the output will extended by added 5 rows, until the interaction will be no, than the loop will
    quit and the statistics calculation can go on"""
    last_index = df.last_valid_index()
    j = 5
    while extend_data_set == "yes":
        j = j + 5
        print(df.head(j))
        extend_data_set = input("Do you want to see still more rows of the Data set?").strip().lower()
    else:
        print("Ok Great - then we go on with Calculating Statistics.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(df)
    popular_month = df['month'].mode()[0]
    print("Most popular month: ", popular_month)

    # display the most common day of week
    popular_day = df['day of week'].mode()[0]
    print("Most popular day: ", popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # mode() for counting the most frequent value
    popular_start_station = df["Start Station"].mode()[0]
    print("Most popular Start Station is: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("Most popular End Station is: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    # groupby method for binding two coloumns
    popular_station_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()

    print("Most popular station combination is: ", popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()

    # Converting of Seconds into the format DAYS:HOUS:MINUTES:SECUNDS
    total_time_seconds = timedelta(seconds=int((total_travel_time)))
    dt = datetime(1, 1, 1) + total_time_seconds

    mean_time_seconds = timedelta(seconds=int((mean_travel_time)))
    d = datetime(1, 1, 1) + mean_time_seconds

    print("The total Trip Duration Time among the regarding the Time Window is: {}:{}:{}:{}.".format(dt.day - 1, dt.hour, dt.minute, dt.second))
    print("The mean Trip Duration Time among the regarding Time Window is: {}:{}:{}:{}.".format(d.day - 1, d.hour, d.minute, d.second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df.value_counts(["User Type"])
    print("Following you see the different counts of User Types listed here:\n", count_user_types, '\n')


    # Display counts of gender
    # Included Logic for Key Error Handling causes by missing Gender Data in Washington Data Set
    try:
        count_gender = df.value_counts(["Gender"])
        print("Following you see the counts on Gender listed here: \n", count_gender, "\n")
    except KeyError:
        print("For Washington no Data about Gender is available.")

    # Display earliest, most recent, and most common year of birth
    # Included Logic for Key Error Handling causes by missing Birth Data in Washington Data Set
    try:
        earliest_birth = int(df["Birth Year"].min())
        print("The earliest Birth Year is: ", earliest_birth)
    except KeyError:
        print("For Washington no Data about earliest Birth Year is available.")

    try:
        most_recent_date = int(df['Birth Year'].max())
        print("The most recent Birth Year is: ",most_recent_date)
    except KeyError:
        print("For Washington no Data about most recent Birth Year is available.")

    try:
        most_common_birth = int(df["Birth Year"].mode())
        print("The most common Birth Year is: ", most_common_birth)
    except KeyError:
        print("For Washington no Data about most common Birth Year is available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()    # creates the filters Data after User Input
        df = load_data(city, month, day)    # loads data from .csv files
        output_snips_of_data(df)            # prints out first 5 rows of the data set and asks of outputting 5 more after each successfully User Input
        station_stats(df)                   # calc of station stats
        time_stats(df)                      # calc of time stats
        trip_duration_stats(df)             # calc of trip duration stats
        user_stats(df)                      # calc of user stats



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
