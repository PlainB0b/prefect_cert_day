import csv
import httpx
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=4, retry_delay_seconds=0.1, cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=1))
def get_temperature(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp

@task(retries=4, retry_delay_seconds=0.1)
def get_rain(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="rain"),
    )
    rain_status = float(weather.json()["hourly"]["rain"][0])
    return rain_status

@task(retries=4, retry_delay_seconds=0.1)
def get_visibility(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="visibility"),
    )
    visibility_status = float(weather.json()["hourly"]["visibility"][0])
    return visibility_status

@task
def write_to_csv(temp: float, rain: float, vis: float):
    with open('weather_metrics.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Temperature', 'Rain', 'Visibility'])
        writer.writerow([temp, rain, vis])

@flow(retries=4)
def fetch_weather_metrics(lat: float, lon: float):
    logger = get_run_logger()

    temp = get_temperature(lat=lat, lon=lon)
    rain = get_rain(lat=lat, lon=lon)
    vis = get_visibility(lat=lat, lon=lon)

    logger.info(f"Temperature: {temp}")
    logger.info(f"Rain: {rain}")
    logger.info(f"Visibility: {vis}")
    logger.info("Writing to csv...")

    write_to_csv(temp=temp, rain=rain, vis=vis)


if __name__ == "__main__":
    fetch_weather_metrics(44.80401, 20.46513)
