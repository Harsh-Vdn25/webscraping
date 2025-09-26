import requests
from datetime import datetime

API_HOST = "open-weather13.p.rapidapi.com"
API_KEY = "82a0be2b4fmsh8563c0ace1898f8p1beaf9jsne9381e10ff0b"

# Kerala districts with latitude and longitude
districts = {
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Kollam": (8.8932, 76.6141),
    "Pathanamthitta": (9.2649, 76.7876),
    "Alappuzha": (9.4981, 76.3388),
    "Kottayam": (9.5916, 76.5223),
    "Idukki": (9.8436, 77.1471),
    "Ernakulam": (10.0356, 76.3675),
    "Thrissur": (10.5276, 76.2144),
    "Palakkad": (10.7867, 76.6548),
    "Malappuram": (11.0730, 76.0743),
    "Kozhikode": (11.2588, 75.7804),
    "Wayanad": (11.6850, 76.1319),
    "Kannur": (11.8745, 75.3704),
    "Kasaragod": (12.5000, 75.2000)
}

for district, (lat, lon) in districts.items():
    url = f"https://{API_HOST}/latlon"
    querystring = {
        "latitude": lat,
        "longitude": lon,
        "lang": "EN"
    }
    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        print(f"Failed to fetch data for {district}: {response.status_code}")
        continue

    data = response.json()

    # Check if weather data is present
    if "weather" in data and len(data["weather"]) > 0:
        weather_info = data["weather"][0]  # first item in the list
        main = weather_info.get("main", "")
        description = weather_info.get("description", "")

        temp = data.get("main", {}).get("temp")
        feels_like = data.get("main", {}).get("feels_like")
        humidity = data.get("main", {}).get("humidity")
        dt = datetime.fromtimestamp(data.get("dt", 0))

        # Convert Kelvin to Celsius if temperature exists
        temp_c = temp - 273.15 if temp is not None else None
        feels_like_c = feels_like - 273.15 if feels_like is not None else None

        print(f"--- {district} ---")
        print(f"Time: {dt}")
        print(f"Temperature: {temp_c:.2f}°C, Feels like: {feels_like_c:.2f}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather: {main}, Description: {description}")
        print("-" * 50)
    else:
        print(f"No data for {district}")
