import sys
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = { 'January' : 1,
           'February' : 2,
           'March' : 3,
           'April' : 4,
           'May' : 5,
           'June' : 6,
           'July' : 7,
           'August' : 8,
           'September' : 9,
           'October' : 10,
           'November' : 11,
           'December' : 12}

WEEKDAYS = {'Monday' : 0,
            'Tuesday' : 1,
            'Wednesday' : 2,
            'Thursday' : 3,
            'Friday' : 4,
            'Saturday' : 5,
            'Sunday' : 6 }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cityChoice = ""
    city = ["chicago", "nyc", "washington"]

    while (cityChoice == ""):
        print("Which city's bikeshare data would  you like to explore?");
        print("Enter \n\t Chicago \n\t NYC \n\t Washington \n\t \"Quit\" to quit the program");
        userInput = input("Enter your choice for the city: ")
        if (userInput.title() == "Quit"):
            sys.exit()
        elif (userInput.lower() in city) :
            cityChoice = userInput.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    monthChoice = ""
    months = set(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    while (monthChoice == ""):
        print("Which month's bikeshare data would  you like to explore?");
        print("Enter \n\t All for all months \n\t Or enter on of the months from January to December\n\t Or enter ""Quit"" to quit the program\n");
        userInput = input("Enter the month: ");
        if (userInput.title() == "Quit") :
            sys.exit()
        elif (userInput.title() in months) or (userInput.title() == "All"):
            monthChoice = userInput.title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    dayChoice = ""
    days = set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    while (dayChoice == ""):
        print("Which day's bikeshare data would  you like to explore?");
        print("Enter \n\t All for all days \n\t Or enter on of the days from Monday to Sunday\n\t Or enter ""Quit"" to quit the program\n");
        userInput = input("Enter the day: ");
        if (userInput.title() == "Quit") :
            sys.exit()
        elif (userInput.title() in days) or (userInput.title() == "All") :
            dayChoice = userInput.title()

    print('-'*40)
    return cityChoice, monthChoice, dayChoice

def display_data(df, display_number_of_rows):
    """
    Displays the data from the dataframe, certain number of rows at a time, until the user stops the display of data.

    Args:
        df - dataframe from which the data is displayed
        display_number_of_rows - The number of rows at a time that the data is displayed

    Returns:
        None
    """

    total_number_of_rows = len(df.index)
    continue_display = ""
    start_row = 0
    end_row = display_number_of_rows;
    print("Displaying " + str(display_number_of_rows) + " rows of data at a time from the data file:\n")
    while (continue_display.lower() != "quit") :
        if  (end_row > total_number_of_rows) :
            end_row = total_number_of_rows
        print(df[start_row:end_row])
        start_row = end_row
        end_row += display_number_of_rows
        continue_display = ""
        while (continue_display.lower() != "continue") and (continue_display.lower() != "quit") :
            continue_display = input("Enter \n\t \"Continue\" to continue to display the data \n\t \"Quit\" to stop the display of the data\n\t ")

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
    df = pd.read_csv(CITY_DATA[city.lower()])

    display_number_of_rows = 5
    display_data(df, display_number_of_rows)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Create a month column
    df['month'] = pd.DatetimeIndex(df['Start Time']).month

    #Create a day of the week column
    df['day-of-week'] = pd.DatetimeIndex(df['Start Time']).weekday

    #Create an hour column
    df['hour-of-day'] = df['Start Time'].dt.hour

    #Create a column containing Start Station and End Station, for each row
    df['Start-End Stations'] = df['Start Station'] + " --> " + df['End Station']
    print(df['Start-End Stations'].head)

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Given a month, filter the data for that month
    if (month.title() != "All") :
        popular_month =  month.title()
        message = "Specified month is: " + popular_month + "\n"
        popular_day = (df.loc[df.month == MONTHS[month.title()], 'day-of-week']).mode()[0]
        message = message + "Popular day in the specified month is: " + str(popular_day) + "\n"

        # if "All" days is specified, determine popular start hour among all days of the specified month
        if (day.title() == "All") :
            popular_start_hour = (df.loc[df.month == MONTHS[month.title()], 'hour-of-day']).mode()[0]
            message = message + "Popular hour among all the days of the specified month is: " + str(popular_start_hour) + "\n"
        # if a week day is specified, determine popular start hour among all the specified week day of the speficied month
        elif (day.title() != "All") :
            popular_start_hour = (df.loc[(df['month'] == MONTHS[month.title()]) & (df['day-of-week'] == WEEKDAYS[day.title()]), 'hour-of-day']).mode()[0]
            message = message + "Specified week day is: " + day.title() + "\n"
            message = message + "Popular hour among specified week day of the specified month is: " + str(popular_start_hour) + "\n"
    # if "All" months is specified, filter the data for all the months
    elif (month.title() == "All") :
        # determine the popular month
        popular_month = df['month'].mode()[0]
        message = "Popular month is: " + str(popular_month) + "\n"
        #determine the popular day among all the months
        popular_day = df['day-of-week'].mode()[0]
        message = message + "Popular day of all the months is: " + str(popular_day) + "\n"
        # if "All" days is specified, determine popular start hour among all days of all the months
        if (day.title() == "All") :
            popular_start_hour = df['hour-of-day'].mode()[0]
            message = message + "Popular hour of all days of all the months is: " + str(popular_start_hour) + "\n"
        # if a week day is specified, determine popular start hour among all the specified week day of the speficied month
        elif (day.title() != "All") :
            message = message + "Specified week day is: " + day.title() + "\n"
            popular_start_hour = (df.loc[df['day-of-week'] == WEEKDAYS[day.title()], 'hour-of-day']).mode()[0]
            message = message + "Popular hour of the specific day, among all the months is: " + str(popular_start_hour) + "\n"

    print(message)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # Given a month, filter the data for that month
    if (month.title() != "All") :

        # if "All" days is specified, determine popular start station, popular end station and popular trip among all days of the specified month
        if (day.title() == "All") :
            popular_start_station = (df.loc[df.month == MONTHS[month.title()], 'Start Station']).mode()[0]
            message = "Popular start station among all the days of the specified month is: " + popular_start_station + "\n"
            popular_end_station = (df.loc[df.month == MONTHS[month.title()], 'End Station']).mode()[0]
            message = message + "Popular end station among all the days of the specified month is: " + popular_end_station + "\n"
            popular_trip = (df.loc[df.month == MONTHS[month.title()], 'Start-End Stations']).mode()[0]
            message = message + "Popular trip among all the days of the specified month is: " + popular_trip + "\n"
        # if a week day is specified, determine popular start station, popular end station and popular trip among all the specified week day of the speficied month
        elif (day.title() != "All") :
            popular_start_station = (df.loc[(df['month'] == MONTHS[month.title()]) & (df['day-of-week'] == WEEKDAYS[day.title()]), 'Start Station']).mode()[0]
            message = "Popular start station among specified week day of the specified month is: " + popular_start_station + "\n"
            popular_end_station = (df.loc[(df['month'] == MONTHS[month.title()]) & (df['day-of-week'] == WEEKDAYS[day.title()]), 'End Station']).mode()[0]
            message = message + "Popular end station among specified week day of the specified month is: " + popular_end_station + "\n"
            popular_trip = (df.loc[(df['month'] == MONTHS[month.title()]) & (df['day-of-week'] == WEEKDAYS[day.title()]), 'Start-End Stations']).mode()[0]
            message = message + "Popular trip among specified week day of the specified month is: " + popular_trip + "\n"
    # if "All" months is specified, filter the data for all the months
    elif (month.title() == "All") :

        # if "All" days is specified, determine popular start station, popular end station and the popular trip among all days of all the months
        if (day.title() == "All") :
            popular_start_station = df['Start Station'].mode()[0]
            message = "Popular start station of all days of all the months is: " + popular_start_station + "\n"
            popular_end_station = df['End Station'].mode()[0]
            message = message + "Popular end station of all days of all the months is: " + popular_end_station + "\n"
            popular_trip = df['Start-End Stations'].mode()[0]
            message = message + "Popular trip of all days of all the months is: " + popular_trip + "\n"
        # if a week day is specified, determine popular start station and the popular trip among all the specified week day of the speficied month
        elif (day.title() != "All") :
            popular_start_station = (df.loc[df['day-of-week'] == WEEKDAYS[day.title()], 'Start Station']).mode()[0]
            message = "Popular start station of the specific day, among all the months is: " + popular_start_station + "\n"
            popular_end_station = (df.loc[df['day-of-week'] == WEEKDAYS[day.title()], 'End Station']).mode()[0]
            message = message + "Popular end station of the specific day, among all the months is: " + popular_end_station + "\n"
            popular_trip = (df.loc[df['day-of-week'] == WEEKDAYS[day.title()], 'Start-End Stations']).mode()[0]
            message = message + "Popular trip of the specific day, among all the months is: " + popular_trip + "\n"

    print(message)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()



    # Given a month, filter the data for that month
    if (month.title() != "All") :
        # if "All" days is specified, determine the total travel time and the average travel time for all days of the specified month
        if (day.title() == "All") :
            number_of_trips = len(df.loc[df.month == MONTHS[month.title()]])
            message = "Total number of trips in all the days of the specified month is: " + str(number_of_trips) + "\n"
            total_travel_time = (df.loc[df.month == MONTHS[month.title()], 'Trip Duration']).sum()
            message = message + "Total travel time in all the days of the specified month is: " + str(total_travel_time) + "\n"
            average_travel_time = total_travel_time/number_of_trips
            message = message + "Average travel time in all the days of the specified month is: " + str(average_travel_time) + "\n"
        # if a week day is specified, determine the total travel time and the average travel time for the specified week day of the speficied month
        elif (day.title() != "All") :
            number_of_trips = len(df.loc[(df['month'] == MONTHS[month.title()]) & (df['day-of-week'] == WEEKDAYS[day.title()])])
            message = "Total number of trips for the specified week day of the specified month is: " + str(number_of_trips) + "\n"
            total_travel_time = (df.loc[(df['month'] == MONTHS[month.title()]) & (df['day-of-week'] == WEEKDAYS[day.title()]), 'Trip Duration']).sum()
            message = message + "Total travel time for the specified week day of the specified month is: " + str(total_travel_time) + "\n"
            average_travel_time = total_travel_time/number_of_trips
            message = message + "Average travel time for the specified week day of the specified month is: " + str(average_travel_time) + "\n"
    # if "All" months is specified, filter the data for all the months
    elif (month.title() == "All") :
        # if "All" days is specified, determine the total travel time and the average travel time for all days of all the months
        if (day.title() == "All") :
            number_of_trips = len(df['Start Station'])
            message = "Total number of trips in all the days of all the months is: " + str(number_of_trips) + "\n"
            total_travel_time = (df['Trip Duration']).sum()
            message = message + "Total travel time in all the days of all the months is: " + str(total_travel_time) + "\n"
            average_travel_time = total_travel_time/number_of_trips
            message = message + "Average travel time in all the days of all the months is: " + str(average_travel_time) + "\n"
        # if a week day is specified, determine the total travel time and the average travel time in the specified week day of all the months
        elif (day.title() != "All") :
            number_of_trips = len(df.loc[df['day-of-week'] == WEEKDAYS[day.title()], 'Start Station'])
            message = "Total number of trips in the specific day of the week, among all the months is: " + str(number_of_trips) + "\n"
            total_travel_time =  (df.loc[df['day-of-week'] == WEEKDAYS[day.title()], 'Trip Duration']).sum()
            message = message + "Total travel time in the specific day of the week, among all the months is: " + str(total_travel_time) + "\n"
            average_travel_time = total_travel_time/number_of_trips
            message = message + "Average travel time in the specific day of the week, among all the months is: " + str(average_travel_time) + "\n"

    print(message)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print("The count of the types of user:")
    print(df['User Type'].value_counts())


    #Display counts of gender
    if ((city.lower() == "chicago") or (city.lower() == "nyc")) :
        print("\nThe count of types of gender:")
        print(df['Gender'].value_counts())
        print("\nThe earliest birth year:")
        print(int(df['Birth Year'][df['Birth Year'].idxmin()]))
        print("\nThe most recent birth year:")
        print(int(df['Birth Year'][df['Birth Year'].idxmax()]))
        print("\nThe most common year of birth:")
        print(int(df['Birth Year'].mode()[0]))


    # TO DO: Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        message = "Specified city is: " + city + "\n"
        message = message + "Specified month is: " + month + "\n"
        message = message + "Specified day is: " + day + "\n\n"
        print(message)
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df, month, day)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
