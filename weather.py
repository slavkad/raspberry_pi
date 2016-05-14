#!/usr/bin/python
import urllib
import urllib2
import json
from pprint import pprint
import datetime
import time
from datetime import timedelta 
import os

# this script will connect to openwearthmap and pull down weather
# weather will then be parsed and based on the hours we want to be notified on
# it will play a sound
#
# future enhancments will be to record sounds for different  weather codes, wind speed, and temp
#
# the goal is to make a "custom" alarm with today's weather
#
# requires mpg123 to be installed

city_id=''
api_key=''
audio_file="path_to_mp3"
url='http://api.openweathermap.org/data/2.5/forecast/city?id=' + city_id + '&units=imperial&APPID=' + api_key
response = urllib.urlopen(url);
data = json.loads(response.read())

hours_to_check=['08','11','14']

now = datetime.datetime.now()
plus24hours = datetime.datetime.now() + timedelta(days=1)  
plus24hours_time = int(time.mktime(plus24hours.timetuple()))

loop_count=0

weather_codes = {
200:'thunderstorm with light rain',
201:'thunderstorm with rain',
202:'thunderstorm with heavy rain',
210:'light thunderstorm',
211:'thunderstorm',
212:'heavy thunderstorm',
221:'ragged thunderstorm',
230:'thunderstorm with light drizzle',
231:'thunderstorm with drizzle',
232:'thunderstorm with heavy drizzle',
300:'light intensity drizzle',
301:'drizzle',
302:'heavy intensity drizzle',
310:'light intensity drizzle rain',
311:'drizzle rain',
312:'heavy intensity drizzle rain',
313:'shower rain and drizzle',
314:'heavy shower rain and drizzle',
321:'shower drizzle',
500:'light rain',
501:'moderate rain',
502:'heavy intensity rain',
503:'very heavy rain',
504:'extreme rain',
511:'freezing rain',
520:'light intensity shower rain',
521:'shower rain',
522:'heavy intensity shower rain',
531:'ragged shower rain',
600:'light snow',
601:'snow',
602:'heavy snow',
611:'sleet',
612:'shower sleet',
615:'light rain and snow',
616:'rain and snow',
620:'light shower snow',
621:'shower snow',
622:'heavy shower snow',
701:'mist',
711:'smoke',
721:'haze',
731:'sand, dust whirls',
741:'fog',
751:'sand',
761:'dust',
762:'volcanic ash',
771:'squalls',
781:'tornado',
800:'clear sky',
801:'few clouds',
802:'scattered clouds',
803:'broken clouds',
804:'overcast clouds',
900:'tornado',
901:'tropical storm',
902:'hurricane',
903:'cold',
904:'hot',
905:'windy',
906:'hail',
951:'calm',
952:'light breeze',
953:'gentle breeze',
954:'moderate breeze',
955:'fresh breeze',
956:'strong breeze',
957:'high wind, near gale',
958:'gale',
959:'severe gale',
960:'storm',
961:'violent storm',
962:'hurricane'
}

def print_message ( hour, weather_id, temp, wind_speed ):
	print "At {0} hours temperature will be {1}F with winds at {2}mph.  Conditions are {3}".format(hour, temp, wind_speed, weather_codes[weather_id])

for item in data['list']:
        line_dt=item['dt']
        time_split= (time.ctime(int(line_dt))).split()
        hour_split= time_split[3].split(":")

        if loop_count == 0:
                print "right now"
                print_message(hour_split[0], item['weather'][0]['id'], item['main']['temp'], item['wind']['speed'])
        if int(line_dt)<= plus24hours_time:
                if hour_split[0] in hours_to_check:
                        print_message(hour_split[0], item['weather'][0]['id'], item['main']['temp'], item['wind']['speed'])
			os.system("mpg123 -q " + audio_file)
        loop_count += 1
