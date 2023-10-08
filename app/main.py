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
    """
    Read from existing API of sunrise sunset
    TODO : add error handling
    :param latitude: Latitude of city
    :param longtitude: Longtitude of city
    :return: Dictionnary of response
    """
    url = get_url(latitude, longtitude)
    response = httpx.get(url)
    json = response.json()
    return json.get("results", {})


def get_parameter_from_api(api: dict, param_name: str):
    """
    Returns parameter value
    TODO : add error handling
    :param api: API that was returned from timedata
    :param param_name: parameter name
    :return: hour and minutes
    """
    sunset = api.get(param_name)
    output = iso_date_as_string_to_datetime(sunset)
    return f"{output.hour}:{output.minute}"


@app.get("/sunrise")
def get_today_sunrise(latitude: float = 31.89825, longtitude: float = 35.01051):
    """
    This function returns sunrise time for today for give coordinates
    :param latitude: Latitude of city, default is Modiin
    :param longtitude: Longtitude of city, default is Modiin
    :return: Time of sunrise
    """
    api = get_api(latitude, longtitude)
    return get_parameter_from_api(api, "sunrise")


@app.get("/sunset")
def get_today_sunset(latitude: float = 31.89825, longtitude: float = 35.01051):
    """
    This function returns sunset time for today for give coordinates
    :param latitude: Latitude of city, default is Modiin
    :param longtitude: Longtitude of city, default is Modiin
    :return: Time of sunset
    """
    api = get_api(latitude, longtitude)
    return get_parameter_from_api(api, "sunset")


if __name__ == "__main__":
    uvicorn.run(app)
