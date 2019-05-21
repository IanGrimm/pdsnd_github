import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Gets user input for city
    city = input('Would you like to see the report for Chicago, New York, or Washington?\n').lower()
    while city not in ['chicago', 'new york', 'washington']:
        city = input('Invalid selection.  Please try again.\n').lower()

    # Gets user input for month
    month = input('Would you like to filter by month? Choose a month, January through June, or \'All\' for no filter.\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input('Invalid selection. Please try again.\n').lower()

    # Gets user input for day of week
    day = input('Would you like to filter by day of the week? Please choose a day of the week, or \'All\' for no filter.\n').lower()
    while day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
        day = input('Invalid selection.  Please try again.\n').lower()

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

    # Loads chosen city file
    df = pd.read_csv(CITY_DATA[city])

    # Converts start times and end times to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extracts month and day of week from the start time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #  Filters by month if 'all' is not entered
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # Filters by day if 'all' is not entered
    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    print('\nThe most common month (by number) was {}\n'.format(str(df['month'].mode()[0])))

    # Displays the most common day of week
    print('\nThe most common day of the week was {}\n'.format(str(df['day_of_week'].mode()[0])))

    # Displays the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print('\nThe most common starting hour was {}\n'.format(str(df['start_hour'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    print('\nThe most commonly used starting station was {}\n'.format(df['Start Station'].mode()[0]))

    # Displays most commonly used end station
    print('\nThe most commonly used ending station was {}\n'.format(df['End Station'].mode()[0]))

    # Displays most frequent combination of start station and end station trip
    df['station_combination'] = df['Start Station'] + ' to ' + df['End Station']
    print('\nThe most frequently used combination of starting and ending stations was {}\n'.format(df['station_combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculates and Displays total travel time
    df['travel_time'] = df['End Time'] - df['Start Time']
    print('\nThe total travel time was {}\n'.format(str(df['travel_time'].sum())))

    # Displays mean travel time
    print('\nThe mean of all travel times was {}\n'.format(str(df['travel_time'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    type_count = df['User Type'].value_counts()
    print('\nThe total counts of each user type were\n', type_count)

    #  Restricts gender and birth year calculations to new york and chicago only
    if city != 'washington':

        # Displays total counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nThe total counts of each gender were\n', gender_count)

        # Displays the earliest, most recent, and most common year of birth
        print('\nThe earliest birth year was {}\n'.format(str(int(df['Birth Year'].min()))))
        print('\nThe most recent birth year was {}\n'.format(str(int(df['Birth Year'].max()))))
        print('\nThe most common birth year was {}\n'.format(str(int(df['Birth Year'].mode()[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays the raw data in 5 record increments if the user chooses the options to display them and breaks
    when the user chooses no
    """
    start_row = 0
    end_row = 5

    raw_data_request = input('\nWould you like to see the raw data? Please choose Yes or No.\n').lower()

    if raw_data_request == 'yes':

        while end_row <= df.shape[0] -1:

            print(df.iloc[start_row:end_row,:])
            start_row = start_row + 5
            end_row = end_row + 5

            raw_data_option = input('\nWould you like to see the next five rows of data? Please choose Yes or No.\n').lower()

            if raw_data_option == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
