import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_name = ['january','february','march', 'april', 'may', 'june']
day_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = str(input('Enter the name of the city: (chicago, new york, washington)')).lower()
        if city in CITY_DATA.keys():
            print('Thank you')
            break
        else:
            print('That\'s not a valid input. Please enter either Chicago, New York or Washington.')
    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Enter the month you are interested in:(january, february, march, april, may, june, or all)')).lower()
        if month in month_name:
        #if month == 'january' or 'february' or'march' or'april'or 'may' or 'june'or 'all':
            print('Thank you')
            break
        elif month == 'all':
            print('Thank you')
            break
        else:
            print('That\'s not a valid input. Please enter the month between January to June.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('\nEnter the day you are interested in: (all, monday, tuesday, ... sunday)')).lower()
        if day in day_name :
            print('Thank you')
            break
        elif day == 'all':
            print('Thank you')
            break
        else :
            print('That\'s not a valid input. Please enter the full name of the days(ex. monday or Monday).')

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
    with pd.read_csv(CITY_DATA[city]) as df:
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name

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
            df = df[df['day_of_week'] == day.title()]

        return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    while True:
        try:
            # display the most common month
            common_month = df['month'].mode()[0]
            # display the most common day of week
            common_day_of_week =df['day_of_week'].mode()[0]

            # display the most common start hour
            # extract hour from the Start Time column to create an hour column
            df['hour'] = df['Start Time'].dt.hour

            # find the most common hour
            common_hour = df['hour'].mode()[0]

            #print results
            print('Most Common month:', month_name[common_month-1])
            print('Most Common day:', common_day_of_week)
            print('Most Common Start Hour:', common_hour)
            break
        except KeyError:
            print('There is no data for this section.')
            break
    print('-'*40)

    print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    while True:
        try:
            # display most commonly used start station
            common_start_station = df['Start Station'].value_counts().keys().tolist()[:1]
            # display most commonly used end station
            common_end_station = df['End Station'].value_counts()[:1]
            # display most frequent combination of start station and end station trip
            common_path = df.groupby(['Start Station', 'End Station']).size().idxmax()

            print('Most Common start station: ', common_start_station)
            print('Most Common end station: ', common_end_station)
            print('Most Common route: ', common_path)
            break
        except KeyError:
            print('There is no data for this section.')
            break

    print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    while True:
        try:
            # display total travel time
            total_travel = df['Trip Duration'].sum()
            total_travel = time_convert(total_travel)
            print('Total travel time: ', total_travel)
            # display mean travel time
            mean_travel = time_convert(df['Trip Duration'].mean())

            print('Mean travel time: ', mean_travel)
            break
        except KeyError:
            print('There is no data for this trip_duration_stats section.')
            break

    print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    while True:
        try:
            # Display counts of user types
            user_types = df['User Type'].value_counts()
            print('Number of users: ', user_types)

            # Display counts of gender
            gender = df['Gender'].value_counts()
            #print('Gender: ', gender)
            # Display earliest, most recent, and most common year of birth
            earliest_birth = df['Birth Year'].min()
            latter_birth = df['Birth Year'].max()
            common_birth = df['Birth Year'].mode()[0]
            print('Birth related information: \n Earliest: {} \n Recent: {} \n Common: {}'.format(int(earliest_birth), int(latter_birth), int(common_birth)))
            break
        except KeyError:
            print('There is no data for user_stats section.')
            break

    print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
    print('-'*40)

def display_raw_data(df):
    """ Presenting options for displaying raw data """
    i = 0
    raw = input("Do you wish to view the data for this result? Enter yes or no...\n").lower()
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Do you wish to see more rows? Enter yes or no...\n").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'. \n").lower()

def time_convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d hours %02d minutes %02d seconds" % (hour, minutes, seconds)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
