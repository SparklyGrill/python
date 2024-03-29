from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
from dataclasses import dataclass

load_dotenv()
api_key = os.getenv('Api_key')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int

def get_lan_lon(city_name, api_key):
    try:
        resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}').json()
        data = resp[0]
        lat = data['lat']
        lon = data['lon']
        return lat, lon
    except (requests.exceptions.RequestException, IndexError):
        return None, None

def get_current_weather(lat, lon, api_key):
    try:
        resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric').json()
        data = WeatherData(
            main = resp.get('weather')[0].get('main'),
            description = resp.get('weather')[0].get('description'),
            icon = resp.get('weather')[0].get('icon'),
            temperature = int(resp.get('main').get('temp'))
        )
        return data
    except (requests.exceptions.RequestException, IndexError):
        return None

def display_weather(city_name):
    lat, lon = get_lan_lon(city_name, api_key)
    if lat is None or lon is None:
        return None
    weather_data = get_current_weather(lat, lon, api_key)
    if weather_data is None:
        return None
    return weather_data

app = Flask(__name__)
port = 3001

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    city = None
    error = None

    if request.method == 'POST':
        city_name = request.form['cityName']
        if not city_name:
            error = 'Please enter the city name'
        else:
            data = display_weather(city_name)
            city = city_name
            if data is None:
                error = 'City not found'

    return render_template('index.html', data=data, city=city, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=port)
