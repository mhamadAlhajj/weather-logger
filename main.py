import os
from dotenv import load_dotenv
import re
import errors 
import api 
import classes as WR

load_dotenv()
weather_api_key = os.getenv("Weather_API_KEY")
geo_api_key = os.getenv("Geo_API_KEY")


def clean_city_name(raw_input):
    if raw_input is None:
        raise ValueError("City name can't be empty.")

    cleaned = re.sub(r"[^A-Za-z \-]", "", raw_input)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if not cleaned:
        raise ValueError("City name can't be empty.")

    return cleaned.title()


def main():
    weather_list = WR.WeatherLog()
    while True:
        command = input(
            "Type 'exit' to stop, 'avg' for average temperature, "
            "'last N' for the last N records, 'find <city>' to filter, 'load' to load weather log,"
            " or press Enter to add another city: "
        ).strip().lower()

        if command == "avg":
            print("Average of temperature: ",weather_list.average_temperature())
            continue
        if command.startswith("load"):
            weather_list.load_from_csv()
            continue
        if command.startswith("last"):
            number_of_records = int(command.split('last')[1])
            for record in weather_list.record_list[-number_of_records:]:
                print(record)
            continue

        if command.startswith("find"):
            find_city = command.split('find')[1].strip()
            index = {row["city"]: row for row in weather_list.record_list}
            if find_city:
                print(index.get(find_city))
            continue
        if command == "exit":
            break

        try:
            city = clean_city_name(input("city name: "))
        except ValueError as e:
            print(e)
            continue

        country_code = input("country code, optional (e.g. LB ): ").strip().lower()
        if country_code and (len(country_code) != 2 or not country_code.isalpha()):
            print("Country code must be 2 letters, e.g. LB. Skipping it.")
            country_code = ""

        try :
            result = api.fetch_weather(city,country_code)
            if result:
                weather_list.add(result)
        except errors.NoMoreAttemptsError as specificError:
            print(specificError)
            break
        except Exception as e:
            print(e)
    weather_list.save_to_csv()


if __name__ == "__main__":
    main()