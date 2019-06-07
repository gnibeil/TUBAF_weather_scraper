'''
This program is part of to get weather data from the website of the TU Bergakademie Freiberg website.
Library to write down weather in different formats.
The extracted data can be written down into an database or a csv file.
In the moment an sqlite database all acquired values from the TU Bergakademie website can be written.
Alternatively the values like for openweathermap.org can be written to a csv file. 
So data over a longer time periode can be accumulated.
'''

import csv
import sqlite3

'''
The function write_csv_openweathermap attaches weather values in the format of the openweathermap data 
format to an csv file
'''
def write_csv_openweathermap(dataitem):
     # preparation of a row for csv in the order of the items of openweathermap.org
     datarow=dataitem[0]+','+str(dataitem[1])+','+str(dataitem[2])+','+str(dataitem[3])+','+str(dataitem[4])+','+str(dataitem[5])+','+str(dataitem[6])+','+str(dataitem[7])+','+str(dataitem[8])+','+str(dataitem[11])+','+str(dataitem[12])+','+'\n'
     # opening of csv output file and attaching of the new row.
     fd = open('weather.csv','a')
     fd.write(datarow)
     fd.close()


'''
The function create_db creates a sqlite database with a table to store the weather values according to the openweathermap.org data format.
'''
def create_db(db_name):
     db = sqlite3.connect(db_name+'.db')
     cursor = db.cursor()
     cursor.execute('''CREATE TABLE weather(timepoint TEXT, latitude REAL, longitude REAL, atitude REAL, 
                    pessure REAL, humidity INTEGER, radiation INTEGER, temp_high REAL, temp_low REAL,
                    temp_soil REAL, wind_speed REAL, wind_dir INTEGER, rain_today REAL, 
                    rain_yn INTEGER)''')
     db.commit()
     db.close()

'''
The function store_entry_db stores a data item to an existing database in the openweathermap.org  data format.
'''
def store_entry_db(dataset,db_name):
     db = sqlite3.connect(db_name+'.db')
     cursor = db.cursor() 
     cursor.execute('''INSERT INTO weather(timepoint, latitude, longitude, atitude, pessure, humidity , radiation, temp_high , temp_low, temp_soil, wind_speed, wind_dir, rain_today, rain_yn)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (dataitem[0:15]))
     db.commit()
     print "Records created successfully";
     db.close()
