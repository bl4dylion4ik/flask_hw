import requests
from geopy import geocoders
import datetime

gn = geocoders.Nominatim(user_agent="application")

weather_api_key = "1196c500700c8b1c6be9233401a36cc5"
kelvin_int = 273.15


class LocationError(Exception):
    def __init__(self, message: str = None, payload=None):
        self.message = message
        self.payload = payload

    def __str__(self):
        return str(self.message)


def get_gp(city: str) -> (int, int):
    location = gn.geocode(city)
    if location is None:
        raise LocationError("Can't find location.")
    else:
        return float(dict(location.raw)['lat']), float(dict(location.raw)['lon'])


def get_list_weather(lat: float, lon: float) -> dict:
    weather = dict()
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minute,hourly,alerts&appid={weather_api_key}")
    for day in response.json()['daily']:
        weather[str(datetime.datetime.utcfromtimestamp(int(day["dt"])).date())] = round(
            float(day["temp"]["day"]) - kelvin_int, 2)
    return weather


def check_valid_date(date: str) -> bool:
    is_valid = True
    try:
        datetime.datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]))
    except ValueError:
        is_valid = False
    return is_valid


def get_weather_date(lat: float, lon: float, date: str) -> str:  # date - "2022-03-16"
    if not check_valid_date(date):
        return "This date is not valid"
    else:
        try:
            gmt_date = datetime.datetime.strptime(date + ' 13:00:00', '%Y-%m-%d %H:%M:%S').timestamp()
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={int(gmt_date)}&appid={weather_api_key}")
            return str(round(float(response.json()["current"]["temp"]) - kelvin_int, 2))
        except:
            return "Sorry the weather for your date is unknown. The service can only show weather for the previous 5 days."
