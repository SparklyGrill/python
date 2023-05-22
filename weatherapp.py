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
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}').json()
    data = resp[0]
    lat = data['lat']
    lon = data['lon']
    return lat, lon

def get_current_weather(lat, lon, api_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )
    return data

def display_weather(city_name):
    lat, lon = get_lan_lon(city_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data

app = Flask(__name__)
port = 3001

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        city_name = request.form['cityName']
        data = display_weather(city_name)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=port)
