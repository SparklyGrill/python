from flask import Flask, render_template, request
from weatherapp import main as get_weather

app = Flask(__name__)
port = 3001

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    city = None
    error = None

    if request.method == 'POST':
        city = request.form['cityName']
        if not city:
            error = 'Please enter the city name'
        else:
            data = get_weather(city)

    return render_template('index.html', data=data, city=city, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=port)
