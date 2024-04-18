import requests
import json
from datadog import initialize, statsd
import time

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

class MakeApiCall:

    def get_data(self, api):
        response = requests.get(api)
        if response.status_code == 200:
            print("Successfully fetched the data")
            response = self.format_values(response.json())
        else:
            print(f"Error: {response.status_code}. Failed to fetch data.")
            print("Response content:", response.content)

    def format_values(self, obj):
        # text = json.dumps(obj, sort_keys=True, indent=4)
        # text_main = obj['main']
        text_feels_like = obj['main']['feels_like']
        text_temp = obj['main']['temp']
        text_humidity = obj['main']['humidity']
        self.submit_values(text_feels_like,text_temp,text_humidity)
        # print(text_main)
        print(text_feels_like)
        print(text_temp)
        print(text_humidity)

    def __init__(self, api):
        print("init function")
        self.get_data(api)
    
    def submit_values(self, feels_like, temp, humidity):
        statsd.gauge('outside.feels_like', feels_like, tags=["source:script.py"])
        statsd.gauge('outside.temp', temp, tags=["source:script.py"])
        statsd.gauge('outside.humidity', humidity, tags=["source:script.py"])

if __name__ == "__main__":
    api_call = MakeApiCall("https://api.openweathermap.org/data/2.5/weather?q=Denver&appid=bdfe3f66d9c0485a948f488338e7747e&units=imperial")
