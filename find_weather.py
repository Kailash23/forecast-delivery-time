from weather import Weather, Unit

def find_weather(city):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(city)
    forecasts = location.forecast
    weather_type = []
    for f in forecasts:
        weather_type.append(f.text)
    return weather_type
    
