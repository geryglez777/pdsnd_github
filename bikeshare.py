import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

"""The three lists bellow are used throughout the code to evaluate or reference user input"""
cities = list(CITY_DATA)
months = ['January','February','March','April','May','June','All']
days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','All']

def input_check(entry, list_to_compare):
    """
    Used to evaluate user input and offer input suggestions when applicable

    Returns:
    "word_match" variable with one of the values bellow:
        - "User input" when input is correct or input suggestion is accepted,
        - "No" when suggestion to wrong input is not accepted
        - "None" when user input is wrong and no input suggestion were offered to user.
    """
    #Variable declaration
    word_list = list_to_compare
    letters_test = {}
    value = 0
    confirmation = ''
    word_match = ''
    pass_value = .16

    if entry.lower() == 'new york': #Makes it easier for users so they dont have to type the word "city" to get a correct entry
        word_match = 'new york city'
    else:
        for word in word_list:
            value = 0
            for letter in word:
                if letter.lower() in entry.lower():
                    value += 1
            letters_test.update({word: word_ratio})

        letters_match = min(letters_test.keys(), key = (lambda k: letters_test[k] ))

        letters_ratio = letters_test[letters_match]
        length_ratio = np.abs((len(entry)/len(letters_match)) -1)


        if len(letters_match) <= 4:
            pass_value = 0.50
        elif len(letters_match) <= 6:
            pass_value = 0.20

        if letters_ratio <= pass_value and length_ratio <= pass_value:
            confirmation = input('Did you mean ' + letters_match.title() + '? y/n\n ')
            if confirmation[0:1].lower() == 'y':
                word_match = letters_match
            else:
                word_match = 'No'
        else:
            word_match = 'None'

    return word_match

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\n' + '-'*40)
    print(' PYTHON PROJECT\n Created by: Gerardo Gonzalez\n Nanodegree Program: Programming for Data Science with python' )
    print('-'*40 + '\n')

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter a city, Chicago, New York or Washington:\n ').strip()
    while city.lower() not in cities:
        city = input_check(city, cities) #use "input_check" function to evaluate the user input.
        if city == 'No':
            city = input('Please, enter a city, Chicago, New York or Washington:\n ').strip()
        elif city == 'None':
            city = input('***That is not a valid city***.\n Please enter a city:\n ').strip()
    city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Enter a month from January to June, use month names. Enter "all" for all months:\n ').strip()
    while month.title() not in months:
        month = input_check(month, months)
        if month == 'No':
            month = input('***That is not a valid month,***\n Please, enter a month from January to June, use month names. Enter "all" for all months:\n ').strip()
        elif month == 'None':
            month = input('***That is not a valid Month.***\n Please enter a Month from January to June, use month names. Enter "all" for all months:\n ').strip()
    if month.lower() == 'all':
        month = month.lower()
    else:
        month = month.title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day of week, use day names, Enter "all" for all days:\n ').strip()
    while day.title() not in days:
        day = input_check(day, days)
        if day == 'No':
            day = input('Please, enter day of week, use day names. Enter "all" for all days:\n ').strip()
        elif day == 'None':
            day = input('***That is not a valid day.***\n Please enter a day, use day names. Enter "all" for all days:\n ').strip()
    if day.lower() == 'all':
        day = day.lower()
    else:
        day = day.title()

    print('-'*40)

    print('SHOWING DATA FOR:\n CITY: {}\n MONTH: {}\n DAY OF WEEK: {}'.format(city.title(), month.title(), day.title()))

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

    if month.lower() != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    def time_to_12h(time_24h):
        """Convert Time from 24 hour format to 12 hour format."""

        time_12h = str(dt.time(time_24h, 0 , 0))
        time_12h = dt.datetime.strptime(time_12h[0:2], '%H')
        time_12h = time_12h.strftime("%I:%M %p")

        return time_12h

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month: -------------> {}'.format(months[popular_month-1]))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week: ---> {}'.format(popular_day))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour: --------------> {}'.format(time_to_12h(popular_hour)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_s_station = df['Start Station'].mode()[0]
    print('Most popular start station: ------> {}'.format(popular_s_station))

    # TO DO: display most commonly used end station
    popular_e_station = df['End Station'].mode()[0]
    print('Most popular end station: --------> {}'.format(popular_e_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    print('Most popular trip: ---------------> {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def seconds_to_hms(seconds):
        """ Use to split seconds into hours, minutes and seconds """

        hours = int(seconds // 3600)
        seconds = seconds % 3600
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        return hours, minutes, seconds

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum() #Trip duration in dataframe is in seconds
    hours, minutes, seconds = seconds_to_hms(total_travel_time) #"seconds_to_hms" function used
    print('TOTAL TRAVEL TIME:\n {} hours\n {} min\n {} sec\n'.format(hours, minutes, seconds))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean() #Trip duration in dataframe is in seconds,
    hours, minutes, seconds = seconds_to_hms(mean_travel_time) #"seconds_to_hms" function used
    if hours == 0:
        print('MEAN TRAVEL TIME:\n {} min\n {} sec'.format(minutes, seconds))
    else:
        print('MEAN TRAVEL TIME:\n {} hours\n {} min\n {} sec'.format(hours, minutes, seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_cnt = (df['User Type'].value_counts())
    print('USER TYPE COUNT:')
    print(user_type_cnt.to_string())
    print(' ')

    # TO DO: Display counts of gender
    try:
        df['Gender'].fillna('Not Defined', inplace=True)
        gender_count = (df['Gender'].value_counts())
        print('GENDER COUNT:')
        print(gender_count.sort_index().to_string())
        print(' ')
    except:
        print('*No data found for Gender in Washington')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('Earliest birth year: -----> {}\nMost recent birth year: --> {}\nMost common birth: -------> {}'.format(earliest_birth_year, most_recent_birth_year, most_common_birth_year))
    except:
        print('*No data found for Birth Year in Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        try:
            see_raw_data = input('Would you like to see 5 lines of raw data: y/n.\n ')
            if see_raw_data[0:1].lower() == 'y':
                raw_data = pd.read_csv(CITY_DATA[city])
                raw_data_columns = list(raw_data.drop(['Unnamed: 0'], axis = 1).columns)
                for index in range(0,raw_data.index.max()+1,5):
                    print(pd.DataFrame(raw_data[raw_data_columns].loc[index: index + 4]))
                    print('\n' + ('-'*40))
                    confirmation = input('Would you like to see the next 5 lines of raw data: y/n.\n ')
                    if confirmation[0:1].lower() != 'y':
                        break
        except:
            print('You have reached the end of the file')
            print('-'*40)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
