##Script to extract and analyse all of NASA's Space Shuttle flights
##All statistics extracted from https://en.wikipedia.org/wiki/List_of_Space_Shuttle_missions
##
##Usage: >python space_shuttle_flights.py
##
##Usage (interactive): >python -i space_shuttle_flights.py
##
##Written by C. Tibbs (Jul 2022)
##

##Import Python packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
import datetime
import calendar
import sys
from http import HTTPStatus
from pathlib import Path
from bs4 import BeautifulSoup
from io import StringIO
import py_local_settings

##Define parameters
shuttle_flights = {}
launch_dates = []

##Define the URL
url = 'https://en.wikipedia.org/wiki/List_of_Space_Shuttle_missions'

##Request the webpage from the URL
r = requests.get(url)

##Check if call was unsuccessful
if r.status_code != HTTPStatus.OK:
    print('Problem with this call...')

##Check if call was successful
elif r.status_code == HTTPStatus.OK:

    ##Parse the data
    bs_r = BeautifulSoup(r.text, 'html.parser')
    
    ##Find the data tables
    tables = bs_r.find_all('table', {'class':'wikitable sortable'})

    ##Convert the data tables to DataFrames
    df1 = pd.read_html(StringIO(str(tables[0])))
    df1 = pd.DataFrame(df1[0])
    
    df2 = pd.read_html(StringIO(str(tables[1])))
    df2 = pd.DataFrame(df2[0])

    ##Check the column names of the two DataFrames match before merging
    for i in range(len(df2.columns)):
        if df1.columns[i] != df2.columns[i]:
            df2.rename(columns={df2.columns[i]:df1.columns[i]}, inplace=True)
        
    ##Combine the two DataFrames
    df = pd.concat([df1,df2], ignore_index=True)

    ##Extract the names of the shuttles
    shuttles = df['Shuttle'].unique()

    ##Calculate and plot the number of flights for each shuttle
    print('')
    print('#'*50)
    print('Number of flights for each Space Shuttle:')
    print(df['Shuttle'].value_counts())
    print('')
    print(df['Shuttle'].value_counts(normalize = True))
    print('#'*50)
    df['Shuttle'].value_counts().plot(kind='bar', colormap='coolwarm', rot=0)
    plt.title('Number of flights for each Space Shuttle')
    plt.ylabel('Number of flights')
    plt.savefig('Number_of_Space_Shuttle_Flights')
    plt.clf()
    
    ##Update date format of the launch dates of each shuttle flight
    for i in df.index:
        ##Extract the launch day, month, and year
        launch_day = df['Launch date'][i].split()[0]
        launch_month = df['Launch date'][i].split()[1]
        launch_year = df['Launch date'][i].split()[2][0:4]

        ##Convert the string launch date to a datetime object
        launch_date_str = launch_day+' '+launch_month+' '+launch_year
        launch_dates = launch_dates + \
                       [datetime.datetime.strptime(launch_date_str, '%d %B %Y')]

    #Add new launch dates as a new column to the dataframe
    df.insert(loc=2, column='Datetime launch date', value=launch_dates)
    
    ##Calculate and plot the landing sites for each Shuttle flight
    df['Landing site'].value_counts()

    ##Deal with the super script comment on the Landing site entries: "Did not land"
    df.replace(to_replace='Did not land[b]', value='Did not land', inplace=True)
    df.replace(to_replace='Did not land [b]', value='Did not land', inplace=True)
    
    df.groupby('Shuttle')['Landing site'].value_counts()
    df.groupby('Shuttle')['Landing site'].value_counts().unstack().plot(kind='bar',\
                                                                        stacked=True, colormap='coolwarm',\
                                                                        rot=0)
    plt.title('Landing sites for each Space Shuttle flight')
    plt.xlabel('')
    plt.ylabel('Number of Landings')
    plt.savefig('Landing_Sites_for_Space_Shuttle_Flights')

   
        
