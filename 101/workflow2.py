import httpx  # requests capability, but can work with async
from prefect import flow, task


@task
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m,temperature_2m,relative_humidity_2m"),
    )
    most_recent_wind = float(weather.json()["hourly"]["windspeed_10m"][0])
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    most_recent_humidity = float(weather.json()["hourly"]["relative_humidity_2m"][0])
    return most_recent_wind, most_recent_temp, most_recent_humidity


@task
def save_weather(wind: float, temp: float, humidity: float):
    with open("weather.csv", "w+") as w:
        w.write(f"{wind},{temp},{humidity}")
    return "Successfully wrote wind, temp and humidity"


@flow
def pipeline(lat: float, lon: float):
    wind, temp, humidity = fetch_weather(lat, lon)
    result = save_weather(wind, temp, humidity)
    return result


if __name__ == "__main__":
    pipeline(51.94, -0.2)
