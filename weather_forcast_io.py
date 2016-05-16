#!/usr/bin/python
import urllib
import urllib2
import json
from pprint import pprint
import datetime
import time
from datetime import timedelta 
import os

api_key=''
coordinates=''

url='https://api.forecast.io/forecast/' + api_key + '/' + coordinates
response = urllib.urlopen(url);
data = json.loads(response.read())

hours_to_check=['08','11','14']

now = datetime.datetime.now()
plus24hours = datetime.datetime.now() + timedelta(days=1)  
plus24hours_time = int(time.mktime(plus24hours.timetuple()))

def print_message ( hour, weather_id, temp, wind_speed, summary ):
	print "At {0} hours temperature will be {2}F with winds at {3}mph.  Chance of rain is {1}% - {4}".format(':'.join(hour), chance_of_rain, temp, wind_speed, summary)

for item in data['hourly']['data']:
        line_dt=item['time']
        time_split= (time.ctime(int(line_dt))).split()
        hour_split= time_split[3].split(":")
	
        if int(line_dt)<= plus24hours_time:
                if hour_split[0] in hours_to_check:
			temp=int(round(item['temperature']))
			temp_str=str(temp)
			windspeed=int(round(item['windSpeed']))
			chance_of_rain=int(round(item['precipProbability']))
			summary=item['summary']
                        print_message(time_split, chance_of_rain, temp, windspeed, summary )
			os.system("mpg123 -q ./Sounds/" + str(hour_split[0]) + "_oclock.mp3")
			os.system("mpg123 -q ./Sounds/" + str(int(temp_str[0]) * 10) + ".mp3")
			if (int(temp_str[1]) > 0 ):
				os.system("mpg123 -q ./Sounds/" + temp_str[1] + ".mp3")
			os.system("mpg123 -q ./Sounds/degrees.mp3")
