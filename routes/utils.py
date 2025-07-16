import os
from math import radians, sin, cos, sqrt, atan2
from datetime import timedelta
import openrouteservice
from openrouteservice import convert
import requests
import os

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
def fetch_route_from_ors(start_coords, end_coords, api_key):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    # GeoJSON expects coordinates in [longitude, latitude]
    coordinates = [start_coords[::-1], end_coords[::-1]]

    payload = {
        "coordinates": coordinates
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()

        try:
            coords = data['features'][0]['geometry']['coordinates']
            waypoints = [{"lat": latlng[1], "lng": latlng[0]} for latlng in coords]

            summary = data['features'][0]['properties']['summary']
            distance = summary['distance'] / 1000  # in km
            duration = timedelta(seconds=summary['duration'])  # as timedelta

            return waypoints, distance, duration

        except (KeyError, IndexError) as e:
            print("Parsing error:", e)
            return None, None, None
    else:
        print("ORS API error:", response.text)
        return None, None, None
