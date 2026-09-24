# weather-logger

A little command-line tool I built to practice a bunch of Python concepts at once: classes, decorators, regex, error handling, file I/O, and testing. You type in a city, it hits the OpenWeatherMap API, and logs the weather to a CSV file you can look back at later.

## What it does

- Fetches live weather for any city (temperature, humidity, description, wind speed)
- Cleans up messy city input (extra spaces, weird casing, stray symbols)
- Retries automatically if the API call fails
- Saves everything to `weather_log.csv`
- Lets you check the average temperature, find a city's past records, or view the last N entries
- Has pytest tests for the core logic (no live API calls in the tests)

## Setup

1. Clone the repo and install the dependencies:
   ```bash
   pip install requests python-dotenv pytest
   ```
2. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api) (covers both the weather and geocoding endpoints).
3. Create a `.env` file in the project root:
   ```
   Weather_API_KEY=your_key_here
   Geo_API_KEY=your_key_here
   ```

## Usage

Run it with:
```bash
python main.py
```

You'll get a prompt where you can:
- Press Enter to log weather for a new city
- Type `avg` to see the average temperature across logged records
- Type `last N` to see the last N records (e.g. `last 3`)
- Type `find <city>` to look up a city's past records
- Type `load` to load previously saved records from the CSV
- Type `exit` to quit (this also saves everything to CSV)

## Project structure

```
main.py       # the interactive CLI loop + city name cleaning
api.py        # API calls, retry decorator, logging decorator
classes.py    # WeatherRecord and WeatherLog classes
errors.py     # custom exceptions
test_validation.py   # pytest tests
```

## Running the tests

```bash
pytest test_validation.py -v
```
