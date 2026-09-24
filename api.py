import requests
from dotenv import load_dotenv
import os
import datetime
import classes as WR
import time
import errors

load_dotenv()
weather_api_key = os.getenv("Weather_API_KEY")
geo_api_key = os.getenv("Geo_API_KEY")

def loc_call(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"the function : {func.__name__} with args {args} , kwargs {kwargs} take {total_time} seconds")
        return result
    return wrapper

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries:
                        print(f"Attempt {attempt}/{max_retries} failed for {func.__name__}")
                        print(f"error message : {e}")
                        time.sleep(delay)
                    else:
                        raise errors.NoMoreAttemptsError(f"All {max_retries} attempts failed for {func.__name__}: {e}")
        return wrapper
    return decorator

@retry_on_failure()
def _get(url, params=None):
    return requests.get(url, params=params)

def get_coordinates(city,country_code=""):
    limit = 1
    query = f"{city},{country_code}" if country_code else city
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit={limit}&appid={geo_api_key}"
    response = _get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return {'city' : city , 'lat':data[0].get('lat') , 'lon':data[0].get('lon')}
        else :
            raise ValueError("No data returned from the API.")
    else :
        raise ValueError(f"API call failed with status code {response.status_code}.")

@loc_call
def fetch_weather(city , country_code=""):
    coordination = get_coordinates(city, country_code)
    if not coordination:
        return None
    params = {'lat':coordination.get('lat') ,'lon':coordination.get('lon'),'appid':weather_api_key,'units':'metric'}
    response = _get('https://api.openweathermap.org/data/2.5/weather', params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            readable_date = datetime.datetime.fromtimestamp(data.get('dt'))
            weather_record = WR.WeatherRecord(
                coordination.get('city'),
                data.get('main').get('temp'),
                data.get('main').get('humidity'),
                data.get('weather')[0].get('description'),
                data.get('wind').get('speed'),
                readable_date
            )
            return weather_record
        else :
            raise ValueError("No data returned from the API.")
    else :
        raise ValueError(f"API call failed with status code {response.status_code}.")