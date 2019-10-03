#!/usr/bin/env python
# coding: utf-8

# In[7]:


"""
Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. 
Bicycle-sharing systems allow users to rent bicycles on a very short-term basis for a price. This allows people to borrow a 
bike from point A and return it at point B, though they can also return it to the same location if they'd like to just go for 
a ride. Regardless, each bike can serve several users per day.

In this project, data provided by Motivate, a bike share system provider for many major cities in the United States, was 
used to uncover bike share usage patterns. You will compare the system usage between three large cities: Chicago, New York City,
and Washington, DC.

https://www.motivateco.com/
"""

import time
import pandas as pd
import numpy as np

pd.options.display.max_rows = 350
#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
dow = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']


# In[8]:


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
        city = input("Which city's data would you like to analyze? (Enter Chicago, New York City or Washington): ")
        
        if city.upper() not in ('CHICAGO', 'NEW YORK CITY', 'WASHINGTON'):
            print('Invalid selection, pleaase enter Chicago, New York City or Washington.')
        else:
            break
    

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to analyze or 'all' for no filter? (Ex. January, February, all, etc.): ")
        
        if month.upper() not in months and month.upper() != 'ALL':
            print('Invalid selection, pleaase enter a value such as January, February, March, etc.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week would you like to analyze or 'all' for no filter? (Ex. Sunday, Monday, all, etc.): ")
        
        if day.upper() not in dow and day.upper() != 'ALL':
            print('Invalid selection, pleaase enter a value such as Sunday, Monday, Tuesday, etc.')
        else:
            break

    print('-'*40)
    return city, month, day


# In[9]:


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
    
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df.rename(columns={'Start Time':'Start_Time', 'End Time': 'End_Time'}, inplace=True)
    

    df['Month'] = df.Start_Time.dt.month_name()
    df['Day'] = df.Start_Time.dt.weekday_name
    
    if month.lower() == 'all' and day.lower() != 'all':
        df = df[df['Day'] == day.title()]
    elif month.lower() != 'all' and day.lower() == 'all':
        df = df[df['Month'] == month.title()]
    elif month.lower() != 'all' and day.lower() != 'all':
        df = df[(df['Month'] == month.title()) & (df['Day'] == day.title())]
    
    df.rename(columns={'Start_Time':'Start Time', 'End_Time': 'End Time'}, inplace=True)

    return df


# In[10]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    print("The most common month is {}.".format(df.groupby(['Month'])['Month'].count().idxmax()))
    
    # display the most common day of week
    print("The most common day of the week is {}.".format(df.groupby(['Day'])['Day'].count().idxmax()))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    start_hour = df.groupby(['Hour'])['Hour'].count().idxmax()

    if start_hour < 12:
        start_hour = '0' + str(start_hour)
    
    print("The most common start hour is {}:00.".format(start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[11]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is {}.".format(df.groupby(['Start Station'])['Start Station'].count().idxmax()))

    # display most commonly used end station
    print("The most commonly used end station is {}.".format(df.groupby(['End Station'])['End Station'].count().idxmax()))

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start and end stations is {}.".format(df.groupby(['Start Station','End Station'])['Start Station'].count().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[12]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time for all customers is {} seconds".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("The mean travel time for all customers is {} seconds".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[14]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of user types are: \n{}\n".format(df['User Type'].value_counts()))    
        
    # Display counts of gender
    if 'Gender' in df.columns:
        print("The counts of gender are: \n{}\n".format(df['Gender'].value_counts())) 
    else:
        print("Gender metrics are not available for this dataset.")

    if 'Birth Year' in df.columns:
        #calculate earliest year of birth
        df = df.dropna().sort_values(by=['Birth Year']).reset_index(drop=True)
        earliest_yob = df['Birth Year'].iloc[0].astype(int)

        #calculate most recent year of birth
        df = df.dropna().sort_values(by=['Birth Year'], ascending=False).reset_index(drop=True)
        most_recent_yob = df['Birth Year'].iloc[0].astype(int)

        #calculate most common year of birth
        most_common_yob = df['Birth Year'].value_counts().idxmax().astype(int)

        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth is {}.".format(earliest_yob))
        print("The most recent year of birth is {}.".format(most_recent_yob))
        print("The most common year of birth is {}.".format(most_common_yob))
    else:
        print("Birth Year metrics are not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[16]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_data = input('\nWould you like to view the raw data? Enter yes or no.\n') 
        if view_data.lower() == 'yes':
            df2 = df.iloc[:,0:len(df.columns)-3]
            print("Printing dataframe and data will be displayed 5 lines at a time...\n")
            start = 0
            while True:
                print(df2.iloc[start:start+5,:])
                user_input = input("Press the enter key to view 5 more lines or 'stop' to stop viewing data: ")
                start += 5
                if user_input.lower() == 'stop':
                    break
            
        restart = input('\nWould you like to restart? Enter yes or any other key to exit.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


# In[ ]:




