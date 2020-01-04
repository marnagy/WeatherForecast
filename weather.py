# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 20:41:27 2020

@author: mnagy
"""

from requests import request
from datetime import datetime

headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }

response = request("GET", "https://freegeoip.app/json/", headers=headers)

respDict = response.json()

latitude = respDict['latitude']
longitude = respDict['longitude']

del headers, response, respDict

DarkSkySecKey = 'd168120e589cdb3dd911da032d27a0d4'

response = request("GET", "https://api.darksky.net/forecast/{}/{},{}?units=si".format(DarkSkySecKey, latitude, longitude))
d = response.json()
del response
try:
    print("Location: {}".format(d['timezone']))
    cur = d['currently']

    print()
    print("Currently:")
    print("Time: {}".format(datetime.fromtimestamp(cur['time'])))
    print("Apparent temperature: {}°C".format(cur['apparentTemperature']))
    print("Temperature: {}°C".format(cur['temperature']))
    print("Wind speed: {} m/s".format(cur['windSpeed']))
    if cur['windSpeed'] > 0:
        wd = cur['windBearing']
        if wd < 45/2 or wd > 360-45/2:
            wd = "N"
        elif wd > 45/2 and wd < 3*45/2:
            wd = "NW"
        elif wd > 3*45/2 and wd < 5*45/2:
            wd = "W"
        elif wd > 5*45/2 and wd < 7*45/2:
            wd = "SW"
        elif wd > 7*45/2 and wd < 9*45/2:
            wd = "S"
        elif wd > 9*45/2 and wd < 11*45/2:
            wd = "SE"
        elif wd > 11*45/2 and wd < 13*45/2:
            wd = "E"
        elif wd > 13*45/2 and wd < 15*45/2:
            wd = "NE"
        print("Wind direction: {}".format(wd))
    print("Humidity: {} %".format(cur['humidity']*100))
    print("Visibility: {} km".format(cur['visibility']))
    print("Summary: {}".format(cur['summary']))

    print()
    hours = 0
    hours = int(input("Set amount of hours: "))
    if hours <= 0:
        raise Exception("Invalid number of hours")
    hours = min(hours, 48)
    print("Hourly:")
    h = d['hourly']
    dataArr = h['data']

    for i in range(hours):
        dat = dataArr[i]
        t = datetime.fromtimestamp(dat['time'])
        print("Time: {}.{}.{} {}".format( t.day, t.month, t.year, t.time()))
        print("Apparent temperature: {}°C".format(dat['apparentTemperature']))
        print("Temperature: {}°C".format(dat['temperature']))
        print()

    print("Powered by Dark Sky. ( https://darksky.net/poweredby )")
except KeyError:
    print("Error type {}: {}".format(d['code'], d['error']))
except:
    print("You're kidding me, right?")
    print()
    print("Powered by Dark Sky. ( https://darksky.net/poweredby )")