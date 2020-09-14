import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# to convert months name to integers while filtering, and check for vaild user input for month
months = {'jan': 1, 'feb' : 2, 'mar' : 3, 'apr' : 4, 'may' : 5, 'june' : 6}

# to check valid user input, and use while data filtering
days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Enter the disered city from: 'chicago', 'new york city', or 'washington' :\n")
        if city in CITY_DATA:
            break
        print("\nYou have entered a wrong value, please try again with exact form ")

    #get user choice for filtering data and get the month or day to by filterd with
    while True:

        #get user input choice for filtering data by day, month, or processing whole data
        choice_for_filtering_data = input("\nEnter 'month' or 'day' for filtering data with particular month or day,"
        " enter 'none' for processing the whole data\n")

        # get user input for month (all, january, february, ... , june)
        if choice_for_filtering_data == 'month':
            month = input("\nwhich month ? jan, feb, mar, apr, may, or june\n")
            if month not in months: #checking for vaild user input for month
                print("\nYou have entered a wrong month value, please try again with correct form as typed")
                continue
            day = 'all'

        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif choice_for_filtering_data == 'day':
            day = input("\nwhich day ? 'Saturday', 'Sunday', 'Monday' , 'Tuesday', 'Wednesday', 'Thursday' , 'Friday'\n" )
            if day not in days : #checking for vaild user input for day of week
                print("\nYou have entered a wrong day value, please try again with correct form as typed")
                continue
            month='all'

        elif  choice_for_filtering_data == 'none':
            day = month = 'all'

        #acting in case of non-vaild user input of choice_for_filtering_data
        else:
            print("\nYou have entered a wrong value, please try again with exact form of 'day', 'month', or 'none'")
            continue
        break #braking while loop in case of valid user inputs

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df=pd.read_csv(CITY_DATA[city]) #creating pandas DataFrame and loading data

    df['Start Time'] = pd.to_datetime(df['Start Time']) #transforming 'Start Time' column in df to datatime

    df['month'] = df['Start Time'].dt.month #creating new column holding the month number

    df['day_of_week'] = df['Start Time'].dt.day_name() #creating new column holding the day of week

    if month != 'all': #filtering data with specified month if applicable
        df = df[ df['month'] == months[month] ]

    if day != 'all': #filtering data with specified month if applicable
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].unique().size  > 1: #checks data that isn't filtered by month
        countingForMonths=df['month'].value_counts(0)
        print("Most common month : {}, Counts = {} times".format(countingForMonths.index[0],countingForMonths.iloc[0]))

     # display the most common day of week
    if df['day_of_week'].unique().size > 1: #checks data that isn't filtered by day
        countingForDays=df['day_of_week'].value_counts(0)
        print("Most common day : {}, Counts = {} times".format(countingForDays.index[0],countingForDays.iloc[0] ))

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    countingForHours = df['hour'].value_counts(0)
    print("Most common hour : {}, Counts = {} times".format(countingForHours.index[0],countingForHours.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    countsForStartSt = df['Start Station'].value_counts(0)
    print("Most commonly start station : {}, Counts : {} times".format(countsForStartSt.index[0],countsForStartSt.iloc[0]))

    # display most commonly used End station
    countsForEndSt = df['End Station'].value_counts(0)
    print("Most commonly End station : {}, Counts : {} times".format(countsForEndSt.index[0],countsForEndSt.iloc[0]))

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip : {} ".format(df.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time : {} seconds'.format(int(df['Trip Duration'].sum())))

    # display mean travel time
    print('Mean travel time : {} seconds '.format(int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    countsForUserTypes = df['User Type'].value_counts(0)
    print("Nmuber of {}s : {}\nNumber of {}s : {}\n".format(countsForUserTypes.index[0],countsForUserTypes.iloc[0],countsForUserTypes.index[1],countsForUserTypes.iloc[1] ) )


    if 'Gender' in df.columns: #checking existence of 'Gender' column in DataFrame

         #Display counts of Genders
        countsForGneder = df['Gender'].value_counts(0)
        print("Nmuber of  {}s : {}\nNumber of {}s : {}\n".format(countsForGneder.index[0],countsForGneder.iloc[0],countsForGneder.index[1],countsForGneder.iloc[1]))

        # Display earliest, most recent, and most common year of birth
        print("Earliest year of birth : {}\nMost recent year of birth : {}\nMost common year of birth : {}"
        "".format(int(df['Birth Year'].min()), int(df['Birth Year'].max()),int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()

        print('\nLoading data.....')
        df = load_data(city, month, day)
        print('Data has been loaded Sucssefully!')

        #display inputs that program will process on
        print('city : {}\nDay : {}\nMonth : {}'.format(city,day,month))
        print('\n','-'*40)

        input("\nPress Enter to continue...") #pausing the program to give user time to examine the answers
        time_stats(df)

        input("\nPress Enter to continue...")
        station_stats(df)

        input("\nPress Enter to continue...")
        trip_duration_stats(df)

        input("\nPress Enter to continue...")
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
