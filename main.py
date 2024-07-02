from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_location(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/')
    data = response.json()
    return data.get('city', 'Unknown'), data.get('region', 'Unknown'), data.get('country_name', 'Unknown')


def get_weather(city):
    api_key = 'a35c1bfdec36dcd1f41f0885d79e66eb'
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    data = response.json()
    return data ['main']['temp'] if 'main' in data else 'Unknown'

@app.route('/api/hello', methods = ['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'guest')
    client_ip =  request.remote_addr
    city, region, country = get_location(client_ip)
    temperature = get_weather(city)
    greeting = (f' Hello, {visitor_name}!, the temperature is {temperature} degrees celcius in {city}, {region}, {country} ')

    user_data = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }
    return jsonify(user_data)

if __name__ == "__main__":
    app.run(debug=True)