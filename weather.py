import json
import time
import requests
import datetime
import os


def get_weather(city, weather_token):
    query_current_weather = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric\
    &appid={}&lang=ru".format(city, weather_token)
    current_file = f"weather/{datetime.date.today().isoformat()}.json"
    if os.path.exists(current_file):
        with open(current_file) as file:
            weather_info = json.load(file)
    else:
        response = requests.get(query_current_weather)
        data = json.loads(response.text)
        weather_info = {"status_code": data["cod"], "city" : data["name"], "wind" : data["wind"]["speed"],
 "Temp_real" : data["main"]["temp"], "Temp_sence" : data["main"]["feels_like"],
 "Temp_range" : (data["main"]["temp_min"], data["main"]["temp_max"])}
        with open(current_file, "w") as file:
            # write data for day
            json.dump(weather_info, file)
            
    return weather_info

def form_weather_text(weather_info:dict):
    template = f"Погода на сегодня:\n\
Город: {weather_info['city']}\n\
Ветер: {weather_info['wind']} m/c\n\
Температура: {weather_info['Temp_real']} С (Ощущается как {weather_info['Temp_sence']}) \n\
Минимальная и максимальная температура на сегодня: \
{weather_info['Temp_range'][0]} --- {weather_info['Temp_range'][1]} C"
    if weather_info["status_code"] != 200:
        template = "Ой, что-то пошло не так. Код ошибки: {}".format(weather_info["status_code"])
    return template
