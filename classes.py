import os 
import csv
class WeatherRecord:
    def __init__(self,city,temperature,humidity,description,wind_speed,timestamp):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.description = description
        self.wind_speed = wind_speed
        self.timestamp = timestamp.strftime('%Y-%m-%d %H:%M')

    def __str__(self):
        return (f"City: {self.city}, Temperature: {self.temperature}°, "
                f"Humidity: {self.humidity}%, Description: {self.description}, "
                f"Wind speed: {self.wind_speed} km/h , timestamp: {self.timestamp}")
    
    def to_dict(self):
        return {"city":self.city , "temperature":self.temperature , "humidity":self.humidity,"description":self.description,"wind speed":self.wind_speed , "timestamp":self.timestamp}


class WeatherLog:
    def __init__(self,filename="weather_log.csv"):
        self.record_list = []
        self.records_by_city = {}
        self.last_saved_id = self._max_id_in_file(filename)
        self.next_id = self.last_saved_id + 1

    def _max_id_in_file(self,filename):
        if not os.path.isfile(filename):
            return 0
        with open(filename,"r",newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            ids = [int(row['id']) for row in reader if row.get('id')]
        return max(ids, default=0)

    def add(self,weather_record):
        record = weather_record.to_dict()
        record['id'] = self.next_id
        self.next_id += 1
        self.record_list.append(record)
        self.records_by_city.setdefault(record.get('city','').lower(), []).append(record)

    def find_by_city(self,city):
        return self.records_by_city.get(city.lower(), [])

    def average_temperature(self):
        if not self.record_list:
            return 0.0
        sum_of_temperature = sum([record.get('temperature') for record in self.record_list])
        average_of_temperature = sum_of_temperature / len(self.record_list)
        return average_of_temperature

    def list_of_records(self):
        for record in self.record_list:
            yield record

    def save_to_csv(self,filename="weather_log.csv"):
        file_exists = os.path.isfile(filename)
        fieldnames = ["id","city","temperature","humidity","description","wind speed","timestamp"]
        new_records = [record for record in self.record_list if record['id'] > self.last_saved_id]
        if not new_records:
            return
        with open(filename,"a",newline="") as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for record in new_records:
                writer.writerow(record)
        self.last_saved_id = max(record['id'] for record in self.record_list)

    def load_from_csv(self , filename = "weather_log.csv"):
        with open(filename,"r",) as csv_file:
            reader = csv.DictReader(csv_file)
            loaded_records = list(reader)
        for record in loaded_records:
            record['id'] = int(record['id'])
        self.record_list = loaded_records
        self.records_by_city = {}
        for record in loaded_records:
            self.records_by_city.setdefault(record.get('city','').lower(), []).append(record)
        self.next_id = max((record['id'] for record in loaded_records), default=0) + 1
        self.last_saved_id = max((record['id'] for record in loaded_records), default=0)
