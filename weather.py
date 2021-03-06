# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 20:41:27 2020

@author: mnagy
"""

from requests import request
from datetime import datetime
from time import sleep
from os import sep
from sys import platform, argv

def Main():

	args = argv
	args.remove(args[0])

	if ArgsCheck(args):
		headers = {
				'accept': "application/json",
				'content-type': "application/json"
				}

		response = request("GET", "https://freegeoip.app/json/", headers=headers)

		respDict = response.json()

		latitude = respDict['latitude']
		longitude = respDict['longitude']

		del headers, response, respDict

		DarkSkySecKey = 0
		SecKeyFilePath = ''

		if platform == 'win32':
			SecKeyFilePath = "SecKey.txt"
		elif platform == 'linux':
			SecKeyFilePath = "/home/marek/python/WeatherApp/SecKey.txt"

		with open(SecKeyFilePath,'r') as file:
			DarkSkySecKey = file.readline()

		response = request("GET", "https://api.darksky.net/forecast/{}/{},{}?units=si".format(DarkSkySecKey, latitude, longitude))
		d = response.json()
		del response
		try:


			printedInfoCount = 0

			# Used for debugging in terminal
			#print("args: {}".format(str(args)))


			print("Location: {}".format(d['timezone']))
			if "-c" in args or len(args) == 0:
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
				printedInfoCount += 1


			if "-h" in args and args.index("-h") < len(args) - 1:
				print()
				hours = int(args[args.index("-h") + 1])
				if hours <= 0:
					raise Exception("Invalid number of hours")
				hours = min(hours, 47)
				print("Hourly:")
				h = d['hourly']
				dataArr = h['data']

				for i in range(1, hours + 1):
					dat = dataArr[i]
					t = datetime.fromtimestamp(dat['time'])
					print("Time: {}.{}.{} {}".format( t.day, t.month, t.year, t.time()))
					print("Apparent temperature: {}°C".format(dat['apparentTemperature']))
					print("Temperature: {}°C".format(dat['temperature']))
					print("Wind speed: {} m/s".format(dat['windSpeed']))
					if dat['windSpeed'] > 0:
						wd = dat['windBearing']
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
					print("Humidity: {} %".format(dat['humidity']*100))
					print("Visibility: {} km".format(dat['visibility']))
					if i < hours:
						sleep(2)
						print()
				printedInfoCount += 1

			if printedInfoCount > 0:
				print()
				print("Powered by Dark Sky. ( https://darksky.net/poweredby )")
		except KeyError:
			print("Error type {}: {}".format(d['code'], d['error']))
		except:
			print("You're kidding me, right?")
			print()
			print("Powered by Dark Sky. ( https://darksky.net/poweredby )")
	else:
		print("Invalid arguments Error")


def ArgsCheck(args: list):
	b = True
	return b

if __name__ == "__main__":
	Main()