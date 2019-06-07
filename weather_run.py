'''
Programm TUBAF_weather_proxy
Tool to scrape weather regulary from from the website of the Interdisziplinary center of TU Bergakademie Freiberg.
The goal of this program is to get weather data from the website of the TU Bergakademie Freiberg.
The extracted data is written down into an database.
Data is accumolated over time.
There is also the option to bush the data to an open network of weather stations.
'''

from lxml import html
import requests
import csv
import sqlite3
import sys
import time
###import daemon 

import libweatherio as ioapi
import libTUBAFstation as stationapi
import lib_push_openweather

'''
After definition of the functions we can now call them, to process the weather data.
The data on the website is updated every 2 minutes. 
We define 2 modes single mode and daemon mode.
In single mode only the current weather value is written to the database.
In daemon mode the current weather value and every following weather value is written to the database.
The daemon mode is also based on the fact that the weather on the website is updated every 2 min.
'''

## old run lines ... should be rewitten

modus=sys.argv[1]

# The following lines allow one call of the actual weather and to write it down into the storage
if modus=='single':
   dataitem=stationapi.get_weather()
   ioapi.write_csv_openweathermap(dataitem)
   #print the data item
   print dataitem

# An alternative is to start the program as an deamon which continously monitors the data and grep's it all 120 seconds.
if modus=='daemon':
    db_name='weather'
    ioapi.create_db(db_name)
    print 'daemon started'
    for i in range(720): #do for one day
        dataitem=stationapi.get_weather()
        print 'weather recived'
        #   write_csv_openweathermap(dataitem)
        ioapi.write_csv_openweathermap(dataitem)
        ioapi.store_entry_db(dataitem,db_name)
        print 'weather written'
        #print the data item
        print dataitem
        time.sleep(120)
        print 'sleep over'
    print 'daemon timed out'
