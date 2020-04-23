from datetime import datetime, timedelta

import pytz
import requests
from pytz import timezone


class WeatherBitIo():
    def __init__(self, lon, lat, apikey=None):
        if apikey is not None:
            self.apikey = apikey
        else:
            self.apikey = '2c5f1fe5b0b041a4bb71caaff44e274d'  # free account api key
        self.lon = lon
        self.lat = lat

    def get_forecast(self):
        self.forecast_url = f"https://api.weatherbit.io/v2.0/forecast/hourly?lat={self.lat}&lon={self.lon}"
        print(self.forecast_url)
        self.forecast_params = {'key': self.apikey}
        resp = requests.get(self.forecast_url, params=self.forecast_params)
        print(resp.json())
        if resp.status_code != 200:
            print('http error number: ', resp.status_code,
                  ', message:', resp.json()['error'])
            return False
        else:
            return_array = []
            for i in resp.json()['data']:
                return_array.append(
                    [i['ts'], i['temp'], i['wind_spd'], i['wind_dir'], i['clouds'], i['ghi'], None])
            return return_array

    def get_historical(self):
        self.forecast_url = f"https://api.weatherbit.io/v2.0/current?lat={self.lat}&lon={self.lon}"
        self.forecast_params = {'key': self.apikey}
        resp = requests.get(self.forecast_url, params=self.forecast_params)
        if resp.status_code != 200:
            print('http error number: ', resp.status_code,
                  ', message:', resp.json()['error'])
            return False
        else:
            return_array = []
            for i in resp.json()['data']:
                return_array.append(
                    [i['ts'], i['temp'], i['wind_spd'], i['wind_dir'], i['clouds'], i['ghi'], None])
            return return_array

    def get_current_weather(self):
        self.current_weather_url = f'https://api.weatherbit.io/v2.0/current?lat={self.lat}&lon={self.lon}'
        self.forecast_params = {'key': self.apikey}
        resp = requests.get(self.current_weather_url,
                            params=self.forecast_params)
        if resp.status_code != 200:
            print('http error number: ', resp.status_code,
                  ', message:', resp.json()['error'])
            return False
        else:
            current_weather_dict = resp.json()['data'][0]
            print(resp.json())
            current_weather_dict = self.localize_converter(
                current_weather_dict)

            return current_weather_dict

    def localize_converter(self, current_weather_dict):

        datetime_from_api = datetime.strptime(
            current_weather_dict['datetime'], '%Y-%m-%d:%H')
        utc_datetime = datetime_from_api.replace(tzinfo=timezone('UTC'))

        localize_datetime = utc_datetime.astimezone(
            timezone(current_weather_dict['timezone']))

        current_weather_dict['datetime'] = localize_datetime
        return current_weather_dict
