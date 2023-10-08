import httpx
import uvicorn
from fastapi import FastAPI
import cachetools

from lib.proceed import get_url, iso_date_as_string_to_datetime

app = FastAPI()
cache = cachetools.TTLCache(maxsize=25, ttl=3600)


@app.get("/")
def hello_world():
    return "Hello, world!"


@cachetools.cached(cache)
def get_api(latitude: float, longtitude: float):
    url = get_url(latitude, longtitude)
    response = httpx.get(url)
    json = response.json()
    return json.get("results", {})


def get_parameter_from_api(api: dict, param_name: str):
    sunset = api.get(param_name)
    output = iso_date_as_string_to_datetime(sunset)
    return f"{output.hour}:{output.minute}"


@app.get("/sunrise")
def get_today_sunrise(latitude: float = 31.89825, longtitude: float = 35.01051):
    api = get_api(latitude, longtitude)
    return get_parameter_from_api(api, "sunrise")


@app.get("/sunset")
def get_today_sunset(latitude: float = 31.89825, longtitude: float = 35.01051):
    api = get_api(latitude, longtitude)
    return get_parameter_from_api(api, "sunset")


if __name__ == "__main__":
    uvicorn.run(app)
