import os
import requests
from geopy.geocoders import Nominatim
from datetime import datetime

x_rapidapi_key = os.environ['RAPIDAPI_KEY']
user_agent = os.environ['U_AGENT']
headers = {
        "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
        "x-rapidapi-key": x_rapidapi_key
    }

class Resp:

    def __init__(self, city, time):
        self._city = city
        self._time = time

    def set_query(self):
        geolocator = Nominatim(user_agent=user_agent)
        location = geolocator.geocode(self._city)
        query = {"cnt": "7", "units": "metric"}
        query["q"] = self._city
        query["lat"] = location.latitude
        query['lon'] = location.longitude
        return query

    @staticmethod
    def nearest_days_resp(frmt, time):
        return f"{time}\n" \
                      f"Weather: {str(frmt['weather'][0]['description'])}\n" \
                      f"Cloudiness: {frmt['clouds']}%\n" \
                      f"Day: {frmt['temp']['day']}, Feels like: {frmt['feels_like']['day']}\n" \
                      f"Night: {frmt['temp']['night']}, Feels like: {frmt['feels_like']['night']}\n" \
                                                        f"Humidity: {frmt['humidity']}%\n" \
                                                        f"Wind: {frmt['speed']} m/s"

    @staticmethod
    def week_forecat_resp(frmt):
        return f"Today: {frmt[0]['temp']['eve']}, {frmt[0]['weather'][0]['description']}\n" \
                      f"Tomorrow: {frmt[1]['temp']['eve']}, {frmt[1]['weather'][0]['description']}\n" \
                      f"{datetime.fromtimestamp(frmt[2]['dt']).strftime('%d %b')}: {frmt[2]['temp']['eve']}, {frmt[2]['weather'][0]['description']}\n" \
                      f"{datetime.fromtimestamp(frmt[3]['dt']).strftime('%d %b')}: {frmt[3]['temp']['eve']}, {frmt[3]['weather'][0]['description']}\n" \
                      f"{datetime.fromtimestamp(frmt[4]['dt']).strftime('%d %b')}: {frmt[4]['temp']['eve']}, {frmt[4]['weather'][0]['description']}\n" \
                      f"{datetime.fromtimestamp(frmt[5]['dt']).strftime('%d %b')}: {frmt[5]['temp']['eve']}, {frmt[5]['weather'][0]['description']}\n" \
                      f"{datetime.fromtimestamp(frmt[6]['dt']).strftime('%d %b')}: {frmt[6]['temp']['eve']}, {frmt[6]['weather'][0]['description']}\n"

    def get_resp(self):
        querystring = self.set_query()
        response = requests.get('https://community-open-weather-map.p.rapidapi.com/forecast/daily',
                                headers=headers, params=querystring).json()
        if self._time == 'Today':
            text = self.nearest_days_resp(response['list'][0], self._time)
        elif self._time == 'Tomorrow':
            text = self.nearest_days_resp(response['list'][1], self._time)
        else:
            text = self.week_forecat_resp(response['list'])
        return text