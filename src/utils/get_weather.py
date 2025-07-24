import requests


def get_weather_data(lat, lon, timestamp):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,wind_speed_10m&start={timestamp}&end={timestamp}"
        f"&timezone=UTC"
    )
    try:
        response = requests.get(url)
        data = response.json()
        temp = data["hourly"]["temperature_2m"][0]
        wind = data["hourly"]["wind_speed_10m"][0]
        return {
            "temperature": temp,
            "wind": wind
        }
    except Exception:
        return {
            "temperature": None,
            "wind": None
        }
