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
import py_local_settings

##Define parameters
shuttle_flights = {}

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
    df1 = pd.read_html(str(tables[0]))
    df1 = pd.DataFrame(df1[0])
    
    df2 = pd.read_html(str(tables[1]))
    df2 = pd.DataFrame(df2[0])
     
    ##Check the column names of the two DataFrames match before merging
    for i in range(len(df2.columns)):
        if df1.columns[i] != df2.columns[i]:
            df2.rename(columns={df2.columns[i]:df1.columns[i]}, inplace=True)
        
    ##Combine the two DataFrames
    df = pd.concat([df1,df2], ignore_index=True)

    ##Extract the names of the shuttles
    shuttles = df['Shuttle'].unique()

    ##Calculate the number of flights for each shuttle
    print('')
    print('#'*50)
    print('Number of flights for each Space Shuttle:')
    for shuttle in shuttles:
        shuttle_df = df[df['Shuttle'] == shuttle]
        shuttle_flights[shuttle] = len(shuttle_df)
        print(shuttle, ':', len(shuttle_df))       
    print('#'*50)
    print('')

    

        
