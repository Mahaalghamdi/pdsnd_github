import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def month_filter():
    """ Ask the user to enter month and test if the user entered a correct month
    Returns: month name if it's correct """
    while True:
        try:
            month=input('\nWhich month? January, Februray, March, April, May, or June? \n')
            months=['january', 'februray', 'march', 'april', 'may', 'june']
            if month not in months:
                raise ValueError
            else:
                return month
            break
        except ValueError:
            print("Invalid input ! Please enter a valid month name that exist in the choices ")
        except KeyboardInterrupt:
            print('There is no input taken ! ')

def day_filter():
    """ Ask the user to enter day and test if the user entered a correct day
    Returns: day number if it's correct """
    while True:
        try:
            day=int(input('\nWhich day? Please type your response as an integer (e.g, 0=Monday  ..etc). \n'))
            days=[0,1,2,3,4,5,6]
            if day not in days:
                raise ValueError
            else:
                return day
            break
        except ValueError:
            print("Invalid input ! Please enter a valid day that exist in the choices ")
        except KeyboardInterrupt:
            print('There is no input taken ! ')

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("\nHello! Let\'s explore some US bikeshare data!")
    while True:
        try:
            # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            city=input("\nWould you like to see data for chicago, new york city or washington ? If you don't want to continue type 'exit' \n ")
            if city.lower() == 'exit':
                # exit from the program
                exit()
            elif city.lower() not in CITY_DATA.keys():
                # if the user didn't chose one of the city choices the program will raise an error
                raise KeyError

            filter=input("\nWould you like to filter by month, day, both, or not at all? Type 'none' for no time filter. If you don't want to continue type 'exit' \n")

            if filter.lower() == 'exit':
                # exit from the program
                exit()
            elif filter.lower() == 'month':
                # get user input for month (all, january, february, ... , june)
                day='all'
                month=month_filter()
            elif filter.lower()=='day':
                # get user input for day of week (all, monday, tuesday, ... sunday)
                month='all'
                day=day_filter()
            elif filter.lower()=='both':
                # get user input for month (all, january, february, ... , june)
                month=month_filter()
                # get user input for day of week (all, monday, tuesday, ... sunday)
                day=day_filter()
            elif filter.lower() == 'none':
                day='all'
                month='all'
            else:
                # if the user didn't chose one of the filter choices the program will raise an error
                raise ValueError
            break

        except KeyError:
            print('Invalid input ! Try Again, You should enter a city that exist in the choices ')
        except ValueError:
            print('Invalid input ! Please enter a proper choice')
        except KeyboardInterrupt:
            print('There is no input taken ! ')

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days[day]
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df,city,month,day):

    """Displays statistics on the most frequent times of travel.

    For specified month : it display the most frequent day and hour of travel
    For specified day : it display the most frequent month and hour of travel
    For all: it display the most frequent month ,day and hour of travel
    For specified month and day : it display the most frequent hour of travel

    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if (month == 'all'):
        print('What is the most popular month of travling ?\n')
        df['month'] = df['Start Time'].dt.month
        common_month = df['month'].mode()[0]
        count_month = df['month'].value_counts().max()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        common_month = months[common_month - 1]
        print('- The most common month of travling is : {} \nCounts : {}'.format(common_month.title(),count_month))

    # display the most common day of week
    if (day == 'all'):
        print('\nWhat is the most popular day of travling ?\n')
        df['day'] = df['Start Time'].dt.dayofweek
        common_day = df['day'].mode()[0]
        count_day = df['day'].value_counts().max()
        days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        common_day = days[common_day]
        print('- The most common day of travling is : {} \nCounts : {}'.format(common_day.title(),count_day))


    # display the most common start hour
    print('\nWhat is the most popular hour of travling ?\n')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    count_hour = df['hour'].value_counts().max()
    hour = " {} AM ".format(common_hour)
    if popular_hour > 12:
       hour= " {} PM ".format(popular_hour - 12)
    print('- The most common hour of travling : {} \nCounts : {}\n'.format(hour,count_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('What is the most popular start station used ?\n')
    common_start_station = df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts().max()
    print("- The most common used start station is :  {}\nCounts : {} ".format(common_start_station,count_start_station))

    # display most commonly used end station

    print('\nWhat is the most popular end station used ?\n')
    common_end_station = df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts().max()
    print("- The most common used end station is :  {} \nCounts : {}".format(common_end_station,count_end_station))

    # display most frequent combination of start station and end station trip
    print('\nWhat is the most popular start and end station used ?\n')
    df['Together']=(df['Start Station']+ " \nEnd Station :  " + df['End Station'])
    common_start_end=df['Together'].mode()[0]
    count_both = df['Together'].value_counts().max()
    print('- The most frequent combination of start station and end station trip are: \n\nStart Station :  {} \nCounts : {}\n'.format(common_start_end , count_both))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('What is the total travel duration ?\n')
    df['Start'] = pd.to_datetime(df['Start Time'])
    df['End'] = pd.to_datetime(df['End Time'])

    hourS=df['Start'].dt.hour.sum()
    hourE=df['End'].dt.hour.sum()

    minS=df['Start'].dt.minute.sum()
    minE=df['End'].dt.minute.sum()

    secS=df['Start'].dt.second.sum()
    secE=df['End'].dt.second.sum()

    dayS=df['Start'].dt.day.sum()
    dayE=df['End'].dt.day.sum()

    difference = timedelta( days = int(dayE) , hours = int(hourE) , minutes = int(minE) , seconds=int(secE)) - timedelta(days = int(dayS) , hours = int(hourS) , minutes = int(minS) , seconds=int(secS))
    print('- The duration total time is : {}\n'.format(difference))

    # display mean travel time
    print('What is the average travel duration ?\n')
    df['Start'] = pd.to_datetime(df['Start Time'])
    df['End'] = pd.to_datetime(df['End Time'])

    hourS=df['Start'].dt.hour.mean()
    hourE=df['End'].dt.hour.mean()

    minS=df['Start'].dt.minute.mean()
    minE=df['End'].dt.minute.mean()

    secS=df['Start'].dt.second.mean()
    secE=df['End'].dt.second.mean()

    dayS=df['Start'].dt.day.mean()
    dayE=df['End'].dt.day.mean()

    days=''
    difference = timedelta(days = dayE, hours = hourE, minutes = minE, seconds=secE) - timedelta(days = dayS, hours = hourS, minutes =minS , seconds=secS)
    if int(dayE) - int(dayS) == 0:
        days='0 days'
        print('- The duration average time is : {} {}\n'.format(days,difference))

    # display longest travel Duration
    print('What is the longest travel duration ?\n')
    start_day=df['Start'].dt.day
    end_day=df['End'].dt.day

    df['duration']= end_day - start_day
    print('- The longest travel duration took : {} days\n'.format(df['duration'].max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('What is the breakdown of users ?\n')
    user_counts = df['User Type'].value_counts()
    print(user_counts)

    # Display counts of gender
    if (city.lower() == 'chicago') or (city.lower() == 'new york city'):
        print('\nWhat is the breakdown of gender ?\n')
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

        # Display earliest, most recent, and most common year of birth
        print('\nWhat is oldest, most youngest, and most common year of birth ?\n')
        print('- The oldest year of birth :      {}'.format(df['Birth Year'].min()))
        print('- The youngest year of birth :    {}'.format(df['Birth Year'].max()))
        print('- The most common year of birth : {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """ Display the data and test if there are user errors """
    df=df.drop(columns=['Start', 'End','duration','Together','hour','month'])
    start = 0
    end = 1
    for i in range(5):
        table=df[start:end].to_dict('index')
        print(table)
        print("\n\n")
        start = start+1
        end=end+1
    while True:
        try:
            i=input("\nWould you like to view individual trip data ? Enter 'yes' or 'no' .\n")
            if i.lower() == 'no':
                break
            elif i.lower() != 'yes':
                raise ValueError
            else:
                for i in range(5):
                    table=df[start:end].to_dict('index')
                    print(table)
                    print("\n\n")
                    start = start+1
                    end=end+1

        except ValueError:
            print('Invalid Input ! You have to choose either yes or no ')
        except KeyboardInterrupt:
            print('There is no input taken ! ')

def main():
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_data(df)
        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() == 'no':
                    break
                elif restart.lower() == 'yes':
                    main()
                else:
                    raise ValueError
                break
            except ValueError:
                print('Invalid Input ! You have to choose either yes or no ')
            except KeyboardInterrupt:
                print('There is no input taken ! ')

if __name__ == "__main__":

	main()
