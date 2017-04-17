"""
Katya Donovan
SoftDes Spring 2017

Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

from urllib.request import urlopen
import json
from pprint import pprint


def get_url(place_name):
	GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
	place_name= place_name.replace(" ", "+")
	url = GMAPS_BASE_URL + "?address=" +place_name
	f = urlopen(url)
	response_text = f.read()
	response_data= json.loads(str(response_text,"utf-8"))
	return response_data

def get_lat_long(response_data):
	"""
	Given a place name or address, return a (latitude, longitude) tuple
	with the coordinates of the given place.

	See https://developers.google.com/maps/documentation/geocoding/
	for Google Maps Geocode API URL formatting requirements.
	"""
	lat = response_data["results"][0]["geometry"]["location"]["lat"]
	lng = response_data["results"][0]["geometry"]["location"]["lng"]
	return lat, lng

def get_nearest_station(latitude, longitude):
	"""
	Given latitude and longitude strings, return a (station_name, distance)
	tuple for the nearest MBTA station to the given coordinates.

	See http://realtime.mbta.com/Portal/Home/Documents for URL
	formatting requirements for the 'stopsbylocation' API.
	"""
	MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
	MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"
	url = MBTA_BASE_URL + "?api_key=" + MBTA_DEMO_API_KEY + "&lat=%s&lon=%s&format=json"%(latitude,longitude)
	f = urlopen(url)
	response_text = f.read()
	response_data= json.loads(str(response_text,"utf-8"))
	station_name = response_data['stop'][0]['stop_name']
	distance = response_data["stop"][0]["distance"]
	return (station_name,distance)


def find_stop_near(place_name):
	"""
	Given a place name or address, print the nearest MBTA stop and the
	distance from the given place to that stop.
	"""
	lat, lng = get_lat_long(get_url(place_name))
	res = get_nearest_station(str(lat),str(lng))
	print("The nearest station to you is " + res[0] + "and it is " + res[1] + "kilometers away.")

find_stop_near("Fenway Park")
