from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

api_key = "a35c1bfdec36dcd1f41f0885d79e66eb"

@app.route('/api/hello', methods=['GET'])
def hello():
    ip = request.headers.get('X-Real-IP')
    if not ip:
        ip = request.remote_addr  # Fallback to remote_addr if X-Real-IP header is not present

    ip_request = f"https://ipapi.co/{ip}/json/"
    location = requests.get(ip_request).json()
    city = location.get("city", "Unknown")
    country = location.get("country", "Unknown")
    long = location.get("longitude", 0)
    lat = location.get("latitude", 0)
    
    weather_request = f"https://api.openweathermap.org/data/2.5/weather"
    header = {
        "lat": lat,
        "lon": long,
        "appid": api_key
    }
    weather = requests.get(url=weather_request, params=header).json()
    temp = int(weather["main"]["temp"])
    celcius = temp - 273.15
    
    visitor_name = request.args.get('visitor_name', default="guest")
    res = {
        "client_ip": ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}! The temperature is {celcius:.2f} degrees Celsius in {city}, {country}"
    }
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)







