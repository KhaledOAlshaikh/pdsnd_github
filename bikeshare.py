import numpy as np
import pandas as pd
import time
import datetime as dt


def get_city():
    """
        Asks of User to choose from three cities to look at data from said cities
        
        Returns:
        
        (str) lwr_city_name - lowercase name of the city
        
    """
    # Creating a list of cities that the user needs to select from
    cities = ["washington","new_york_city","chicago"]
    
    # Creating an empty string of variable 'lwr_city_name' to make lower case
    lwr_city_name = ""
    
    # Loop to keep asking user for valid input of cities for which data is available
    while lwr_city_name not in cities:
        city_name = str(input("\nEnter either Washington, New York City, or Chicago to see data from those cities: "))
        
        # Adding "_" in place of spaces for path file, specifically for 'New York City'
        lwr_city_name = city_name.lower().replace(" ", "_")
        
        # Failsafe incase user enters non-string value
        if lwr_city_name in cities:
            print(f"\n{city_name.title()} it is.")
            print("_"*100)
        else:
            # Failsafe incase user enters city that's not in the list 'cities'
            print(f"\nLooks like {city_name} is not a vaild city name. Please enter a valid city name")
            continue
    
    # Returns lwr_city_name and assigns it to the variable 'city' in the 'get_data' function
    return lwr_city_name

def get_month():
    """
        Asks of User to choose a month from the list of months to look at data from said months
        
        Returns:
        
        (str) lwr_month - lowercase month
    
    """
    # Creating a list of months, including "All"
    months = ["january", "february", "march", "april", "may", "june", "all"]
    
    # Creating an empty string of variable 'lwr_month' to make lower case
    lwr_month = ""
    
    # Loop to keep asking user for valid input
    while lwr_month not in months:
        month = str(input("\nEnter any month from January to June, if you\'d like to see all of the months please type \"All\": "))
        lwr_month = month.lower()
        
        # Failsafe incase user enters non-string value 
        if lwr_month.isalpha():
            if lwr_month in months:
                print(f"\n{month.title()} it is.")
                print("_"*100)
            else:
                # Failsafe incase user enters month that's not in the list 'months'
                print(f"\nLooks like {month.title()} is not a valid month. Please enter a valid month")
        else:
            print(f"\nLooks like you entered a non-string value. Please enter a valid month")
    
    # Returns lwr_month and assigns it to the variable 'month' in the 'get_data' function
    return lwr_month

def get_day():
    """
        Asks of User to choose a day of the week to look at data from said days
        
        Returns:
        
        (str) lwr_day - lowercase day of the week
        
    """
    # Asks of User to choose a day of the week or all to look at data from said days
    # Creating a list of days, including "All"
    valid_day_inputs = [0,1,2,3,4,5,6,7]
    days = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday", 7 : "all"}
    
    # Creating an empty string of variable 'lwr_day' to make lower case
    day = 8
    # Loop to keep asking user for valid input
    try:
        while day not in valid_day_inputs:
            day = int(input("\nEnter the day of the week you\'d like the data to be from (Please write it in the form of an integer, \'0\' representing \"Monday\", \'1\' representing \"Tuesday\", etc.), \nif you\'d like the whole week please enter \"7\": "))
            if day in valid_day_inputs:
                print(f"\n{days[day].title()} it is.")
                print("_"*100)
                break
            else:
                print(f"\nLooks like you didn\'t enter a valid value. Please enter a a valid day.")
                continue
    except ValueError:
        print(f"\nLooks like you entered a non-integer value. Please enter a valid integer.")
    
    # Returns lwr_day and assigns it to the variable 'day' in the 'get_info' function
    return day

def get_info(city, month, day):
    """
        Loads data for the specified city and filters by month and day if applicable.

        Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
        Returns:
        data - Pandas DataFrame containing city data filtered by month and day
    """
    
    print("\nLoading data...")
    data = pd.read_csv(city + '.csv')
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['month'] = data['Start Time'].dt.month
    data["day_of_week"] = data["Start Time"].dt.weekday
    
    if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            data = data[data['month'] == month]
            
    if int(day) != 7:
        data = data[data["day_of_week"] == int(day)]
    
    print("Data loaded successfully")
    print("_"*100)
    return data


def pop_time(df, dict):
    """
        Performs the necessary calculations to get the most popular times of travel
        
        Args:
        (Dataframe) df - Pandas Dataframe containing the data filtered by user input
        (dict) dict - dictionary containing the user input of 'yes' or 'no' values, 
                        depending if they want to see this info or not
    """
    
    if dict[0] != 'no':
        print("\nCalculating most popular time...")
        
        stopwatch = time.time()
        
        # Displays the most popular fhour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print("\nThe most popular starting hour: " + str(popular_hour))
        
        # Displays the most popular month
        monthdict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"june"}
        popular_month = df['month'].mode()[0]
        print("The most popular month: " + monthdict[popular_month])
        
        # Displays the most popular day of the week
        daydict = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
        popular_day = df['day_of_week'].mode()[0]
        print("The most popular day: " + daydict[popular_day])
        
        # Displays how much it took to calculate the previous calculations
        print(f"\nThis process took {(time.time() - stopwatch)} seconds.")
        print("_"*100)

def pop_stations(df, dict):
    """ 
        Performs the necessary calculations to get the most popular stations
        
        Args:
        (Dataframe) df - Pandas Dataframe containing the data filtered by user input
        (dict) dict - dictionary containing the user input of 'yes' or 'no' values, 
                        depending if they want to see this info or not
    """
    if dict[1] != 'no':
        print("\nCalculating station data...")
        stopwatch = time.time()
        
        # Displays the most popular starting station
        popular_start_station = df['Start Station'].mode()[0]
        print("\nThe most popular starting station: " + popular_start_station)
        
        # Displays the most popular ending station
        popular_end_station = df['End Station'].mode()[0]
        print("The most popular ending station: " + popular_end_station)
        
        # Displays the most popular routes
        popular_trips = df[["Start Station", "End Station"]].apply(" to ".join, axis=1).mode()[0]
        print("The most popular trips: " + str(popular_trips))
        
        # Displays how much it took to calculate the previous calculations
        print(f"\nThis process took {(time.time() - stopwatch)} seconds.")
        print("_"*100)
    else:
        pass

def travel_times(df, dict):
    """
        Performs the necessary calculations to get the most popular travel times
    
        Args:
            (Dataframe) df - Pandas Dataframe containing the data filtered by user input
            (dict) dict - dictionary containing the user input of 'yes' or 'no' values, 
                            depending if they want to see this info or not
    """
    if dict[2] != 'no':
        print("\nCalculating travel times data...\n")
        stopwatch = time.time()
        
        # Calculating and displaying the total travel times in hours, minutes and seconds
        tot_travel_times = df['Trip Duration'].sum()
        tot_mins =  tot_travel_times // 60
        tot_hrs = tot_mins // 60
        
        print(f"The total travel time: {int(tot_hrs // 1)} hour(s), {int((tot_mins % 60) // 1)} minute(s), and {int((tot_travel_times % 60) // 1)} seconds" )
        
        # Calculating and displaying the average travel times in hours, minutes and seconds
        avg_travel_times = df['Trip Duration'].mean()
        avg_mins = avg_travel_times // 60
        
        print(f"The average travel time: {int((avg_mins % 60) // 1)} minute(s), and {int((avg_travel_times % 60) // 1)} seconds" )
        
        
        print(f"\nThis process took {(time.time() - stopwatch)} seconds.")
        print("_"*100)

def user_info(df, dict, city_name):
    """
        Performs the necessary calculations to get the user information
    
        Args:
            (Dataframe) df - Pandas Dataframe containing the data filtered by user input
            (dict) dict - dictionary containing the user input of 'yes' or 'no' values
            (str) city_name - name of city
    """
    
    if dict[3] != 'no':
        print("\nCalculating user information data...\n")
        stopwatch = time.time()
        
        # Displays the total count of users and user types
        user_type = df['User Type'].value_counts()
        print(f"The user type count: \n{user_type}")
        
        if city_name == "new_york_city" or city_name == "chicago":
            # Displays the count of total users based on gender
            gender_cnt = df['Gender'].value_counts()
            print(f"\nThe user Gender count: \n{gender_cnt}")
            
            # Displays the youngest, oldest and most common years
            min_year = df['Birth Year'].min()
            max_year = df['Birth Year'].max()
            common_year = df['Birth Year'].mode()[0]
            print(f"\nThe oldest year: {int(min_year)}")
            print(f"The youngest year: {int(max_year)}")
            print(f"The most common year: {int(common_year)}")
        else:
            pass
        
        print(f"\nThis process took {(time.time() - stopwatch)} seconds.")

def more_data(df):
    """ 
    Ask user if they want to see more raw data
    
    Args:
        (str) ans - string containing the user input of 'yes' or 'no' 
    """
    
    ans = str(input('\n\nWhat would you like to see 5 lines of raw data? (Please enter either \'yes\' or \'no\'): '))
    n = 0
    if ans == 'yes':
        print(df.iloc[n:n+5])
        n += 5
        answer = ""
        while True:
            answer = str(input('\n\nWould you like to see 5 more lines of raw data? (Please enter either \'yes\' or \'no\'): '))
            if answer.lower() == 'yes':
                print("Printing 5 rows of raw data")
                print(df.iloc[n:n+5])
                n += 5
            elif answer.lower() == 'no':
                break
            else:
                print("Please enter a valid answer (yes or no)")
                continue
    else:
        pass

def get_data():
    """
        Calls other functions to get the necessary based on user input
    
    """
    print("\nHello, User! Welcome to Khaled Alshaikh\'s Udacity Project Submission. \n\nLet\'s explore some data!")
    # Assigns city, month, and day to the functions "get_city", "get_month", and "get_day respectively
    city = str(get_city())
    month = str(get_month())
    day = str(get_day())
    
    # Creating a list of functions that can be looped through
    questions = ["the most popular days and months", "the most popular stations", "info about travel times", "user information data"]
    # Creating an empty dictionary to hold answers from users about questions
    dict = {}
    # Creating a variable called "z" and assigning it to the value of zero so it can hold the index of each question
    z = 0
    for x in questions:
        while True:
            y = input("\nWould you like to see " + x + "?. Please reply with \"Yes\" or \"No\": ")
            if y.lower() == 'yes' or y.lower() == 'no':
                dict[int(z)] = str(y.lower())
                z += 1
                break
            else:
                print(y + " is not a valid answer.")
                continue
    df = get_info(city, month, day)
    pop_time(df, dict)
    pop_stations(df,dict)
    travel_times(df, dict)
    user_info(df, dict, city)
    more_data(df)

if __name__ == '__main__':
    # Code starts here by calling start_program() to start the program to take user input
    def start_program():
        get_data()
        while True:
            answer = input("\nThank you so much for using this program. \nWould you like to restart this program? Please answer with \"Yes\" or \"No\": ")
            if answer.lower() == 'yes':
                start_program()
            elif answer.lower() == 'no':
                print("\nHave a good day!\n")
                break
            else:
                print(answer + "is not a valid answer.")
                continue
            break
    start_program()