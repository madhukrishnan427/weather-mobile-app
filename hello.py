import datetime as dt
import requests
import os
import sys

# ---------------- CONFIGURATION ---------------- #
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY = input("Enter the city name: ")

# Read API key from environment variable
API_KEY = '75362ff2d778a394dd1b6ad11388a0c9'

if not API_KEY:
    print("ERROR: API key not found. Set OPENWEATHER_API_KEY environment variable.")
    sys.exit()

# ---------------- FUNCTIONS ---------------- #
def kelvin_to_celsius_fahrenheit(kelvin):
    """
    Converts temperature from Kelvin to Celsius and Fahrenheit
    """
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    return celsius, fahrenheit


def fetch_weather(city):
    """
    Fetch weather data from OpenWeatherMap API
    """
    params = {
        "q": city,
        "appid": API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("Error fetching weather data. Please check city name or internet connection.")
        sys.exit()

    return response.json()


# ---------------- MAIN LOGIC ---------------- #
def main():
    weather_data = fetch_weather(CITY)

    temp_kelvin = weather_data["main"]["temp"]
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

    feels_like_kelvin = weather_data["main"]["feels_like"]
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)

    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    description = weather_data["weather"][0]["description"].title()

    timezone_offset = weather_data["timezone"]
    sunrise = dt.datetime.utcfromtimestamp(weather_data["sys"]["sunrise"] + timezone_offset)
    sunset = dt.datetime.utcfromtimestamp(weather_data["sys"]["sunset"] + timezone_offset)

    print("\n---------------- WEATHER REPORT ----------------")
    print(f"City            : {CITY}")
    print(f"Temperature     : {temp_celsius:.2f} °C | {temp_fahrenheit:.2f} °F")
    print(f"Feels Like      : {feels_like_celsius:.2f} °C | {feels_like_fahrenheit:.2f} °F")
    print(f"Humidity        : {humidity}%")
    print(f"Wind Speed      : {wind_speed} m/s")
    print(f"Weather         : {description}")
    print(f"Sunrise Time    : {sunrise}")
    print(f"Sunset Time     : {sunset}")
    print("------------------------------------------------\n")


if __name__ == "__main__":
    main()