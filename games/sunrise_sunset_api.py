import httpx
from datetime import datetime
import time


def get_url(lat: float, lng: float) -> str:
    # &date=2023-09-15
    _url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0"
    return _url


def get_current_tz() -> str:
    now = datetime.datetime.now()
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    print(local_tz)
    local_tzname = local_tz.tzname(local_now)
    return local_tzname


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def iso_date_as_string_to_datetime(iso_date: str) -> datetime:
    datetime_obj = datetime.fromisoformat(iso_date)
    return datetime_from_utc_to_local(datetime_obj)


LAT = 31.89825
LNG = 35.01051
url = get_url(LAT, LNG)
response = httpx.get(url)

from pprint import pprint as print

print(response.json())
temp_json = response.json()
print(temp_json.get("status"))
sunset = temp_json.get("results", {}).get("sunset")
print(iso_date_as_string_to_datetime(sunset))
