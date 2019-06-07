'''
The goal of this program is to get weather data from the website of the TU Bergakademie Freiberg website.
The extracted data is written down into an database.
So data over time can be accumulated.
There is also the option to push the data to an open network of weather stations.
'''
######!/usr/bin/python

from lxml import html
import requests

'''
The function get_weather pulls the current version of the weather side of TU Bergakademie Freiberg  weather station at Reiche Zeche.
It extracts the data from there the different parameters which are measured and displayed on the website of the interdisciplanary center of TU Bergakademie Freiberg.
Script has to go through the side to find all data items.
'''  
def get_weather():
     # aquire data
     try: 
         ### old page url in the time of first development of this code
	 ## page = requests.get('http://www.chemie.tu-freiberg.de/wetterdaten/index_tu.php')
	 ## new page url from June 2016
	 page = requests.get('http://www.chemie.tu-freiberg.de/wetterdaten/index2.php')
     except:
         print 'service could not be reached'
     # extract data & restructure data
     tree = html.fromstring(page.text)
     # extract the different data fields from the php code:
     # temperatures
     temperatures= tree.xpath('//div[@class="temp"]/text() ') 
     # wind data
     wind= tree.xpath('//div[@class="windgeschwindigkeit"]/text()')
     # date and time
     datetime = tree.xpath('//div[@class="dattime"]/text()')
     # properties of air
     air = tree.xpath('//div[@class="luft"]/text()')
     # data about rain fall
     rainfall = tree.xpath('//div[@class="niederschlag"]/text()')
     # data rain yes/noch
     rain_check = tree.xpath('//div[@style="visibility:visible"]/text()')
     # extraction of the final values
     # date
     date=datetime[0].encode('ascii', 'replace').split('???')[0].split(' ')[len(datetime[0].encode('ascii', 'replace').split('???')[0].split(' '))-1]
     # time
     time=datetime[0].encode('ascii', 'replace').split('???')[1].split(' ')[0]
     timepoint=date.split('.')[2]+'-'+date.split('.')[1]+'-'+date.split('.')[0]+' '+time
     # altitude
     alt=int(datetime[0].encode('ascii', 'replace').split(':')[2].split('?')[0].split(' ')[len(datetime[0].encode('ascii', 'replace').split(':')[2].split('?')[0].split(' '))-1])
     # latitude (hopefully does not change to dramatically) was manually added acording to the website
     lat=float(50.928333)
     # longitude (hopefully does not change to dramatically) was manually added acording to the website
     lon=float(13.358056)
     # pressure
     pressure=float(air[0].encode('ascii', 'replace').split('?')[0].split(' ')[len(air[0].encode('ascii', 'replace').split('?')[0].split(' '))-1])
     # relative humidity
     humidity=int(air[0].encode('ascii', 'replace').split('?')[1].split(' ')[len(air[0].encode('ascii', 'replace').split('?')[1].split(' '))-1])
     # radistion energy
     radiation=int(air[1].encode('ascii', 'replace').split('?')[0].split(' ')[len(air[1].encode('ascii', 'replace').split('?')[0].split(' '))-1])
     # temperature 2 m above the ground
     temp_high=float(temperatures[0].encode('ascii', 'replace').split('??')[0].split(' ')[len(temperatures[0].encode('ascii', 'replace').split('??')[0].split(' '))-1])
     # temperature 5 cm above the ground
     temp_low=float(temperatures[0].encode('ascii', 'replace').split('??')[1].split(' ')[len(temperatures[0].encode('ascii', 'replace').split('??')[1].split(' '))-1])
     # temperature 10 cm below the ground
     temp_ground=float(temperatures[0].encode('ascii', 'replace').split('??')[2].split(' ')[len(temperatures[0].encode('ascii', 'replace').split('??')[2].split(' '))-1])
     # wind speed in km/h
     wind_speed2=float(wind[0].encode('ascii', 'ignore').split('\t')[1].split(' ')[len(wind[0].split('\t')[1].split(' '))-1])
     # Wind direction
     wind_dir=int(wind[0].split('\t')[3].encode('ascii', 'ignore').split('\n')[0].split(' ')[len(wind[0].split('\t')[3].encode('ascii', 'ignore').split('\n')[0].split(' '))-1])
     # wind speed in m/s
     wind_speed=float(rainfall[0].split('\n')[1].split(' ')[4].encode('ascii', 'ignore').split('m')[0])
     # rain fall Yes/No ?
#     rainyn=rainfall[0].split(':')[1].split('\r')[0]
     rainyn=rain_check[0].split(':')[1].strip()
     # rain fall till mid night
     rain_today=float(rainfall[1].split(':')[1].encode('ascii', 'ignore').split('m')[0]) 
     # daten as vector
     dataitem=[timepoint,lat,lon,alt,pressure,humidity,radiation,temp_high,temp_low,temp_ground,wind_speed,wind_dir,rain_today,rainyn]
     return dataitem

