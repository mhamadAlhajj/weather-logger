from datetime import datetime

import pytest
import requests

import api
import errors
import classes as WR
from main import clean_city_name


def test_clean_city_name():
    assert clean_city_name("Paris") == "Paris"

    assert clean_city_name("  new   york ") == "New York"

    assert clean_city_name("Paris123") == "Paris"
    assert clean_city_name("New York!!") == "New York"

    assert clean_city_name("winston-salem") == "Winston-Salem"

    with pytest.raises(ValueError):
        clean_city_name("123456")

    with pytest.raises(ValueError):
        clean_city_name("   ")

    with pytest.raises(ValueError):
        clean_city_name("")

def test_weather_record_to_dict():
    ts = datetime(2024, 1, 1, 12, 30)
    record = WR.WeatherRecord("Paris", 22.5, 55, "Clear sky", 3.6, ts)

    assert record.to_dict() == {
        "city": "Paris",
        "temperature": 22.5,
        "humidity": 55,
        "description": "Clear sky",
        "wind speed": 3.6,
        "timestamp": "2024-01-01 12:30",
    }


def test_save_and_load_records(tmp_path):
    filepath = str(tmp_path / "weather_log.csv")

    log = WR.WeatherLog(filename=filepath)
    records = [
        WR.WeatherRecord("Paris", 22.5, 55, "Clear sky", 3.6, datetime(2024, 1, 1, 12, 30)),
        WR.WeatherRecord("Beirut", 28.0, 40, "Sunny", 1.2, datetime(2024, 1, 2, 9, 0)),
    ]
    for record in records:
        log.add(record)
    log.save_to_csv(filepath)

    loaded_log = WR.WeatherLog(filename=filepath)
    loaded_log.load_from_csv(filepath)

    assert len(loaded_log.record_list) == len(records)
    for original, loaded in zip(records, loaded_log.record_list):
        assert loaded["city"] == original.city
        assert float(loaded["temperature"]) == original.temperature
        assert int(loaded["humidity"]) == original.humidity
        assert loaded["description"] == original.description
        assert float(loaded["wind speed"]) == original.wind_speed
        assert loaded["timestamp"] == original.timestamp


def test_retry_decorator():
    call_count = {"n": 0}

    @api.retry_on_failure(max_retries=3, delay=0)
    def flaky():
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise requests.exceptions.RequestException("simulated failure")
        return "success"

    assert flaky() == "success"
    assert call_count["n"] == 3


def test_retry_decorator_exhausted():
    @api.retry_on_failure(max_retries=2, delay=0)
    def always_fails():
        raise requests.exceptions.RequestException("simulated failure")

    with pytest.raises(errors.NoMoreAttemptsError):
        always_fails()
