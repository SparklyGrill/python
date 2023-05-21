import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
api_key = os.getenv('Api_key')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int
def get_lan_lon(city_name, Api_key):
    #resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q{city_name}&appid={Api_key}').json()
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={Api_key}').json()
    #data = resp
    #lat = data.get('lat')
    #lon = data.get('lon')
    print(resp)
    data = resp[0]
    lat = data['lat']
    lon = data['lon']
    return lat, lon

def get_current_weather(lat, lon, Api_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=ab81ca23a1a3029e43740ff17cb0a40e&units=metric').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )

    return data

def main(city_name):
    lat, lon = get_lan_lon('Zagreb,hr', api_key)
    get_current_weather(lat, lon, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data

if __name__ == "__main__":
    lat, lon = get_lan_lon('Zagreb,hr', api_key)
    print(get_current_weather(lat, lon, api_key))