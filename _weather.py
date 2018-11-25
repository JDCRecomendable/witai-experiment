"""
Extension of Chatbot for processing Weather Intents
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
"""

# Prerequisites
from random import randrange
import __time
from weather import Weather, Unit
# documentation at https://pypi.org/project/weather-api/
weather = Weather(unit=Unit.CELSIUS)

# Wit API Centric Functions
def get_location(resp):
    """Return the location. If no location is found, returns None.
    
    Parameters:
    resp -- response from Wit.ai
    """
    try:
        return resp['entities']['location'][0]['value']
    except KeyError:
        return None

def get_datetime(resp):
    """Return the datetime. If no datetime is found, returns None.
    
    Parameters:
    resp -- response from Wit.ai
    """
    try:
        return resp['entities']['datetime'][0]['values'][0]['value']
    except KeyError:
        return None

# Invalid Location
def message_invalid_location():
    """Return a string to tell the user that the location inputted in the
    chatbot is invalid.
    """
    return 'Unforunately, only valid cities or its suburbs (if applicable) are supported at the moment. Perhaps, you mispelled the city, or entered a whole country, state or province?'

# Invalid Time (too far ahead)
def message_too_far_ahead():
    """Return a string to tell the user that the datetime inputted in the
    chatbot is too far ahead for a weather prediction.
    """
    digit = randrange(3)
    if digit == 0:
        return 'That is pretty far ahead. Scientists do not have data for weather in that time.'
    elif digit == 1:
        return 'The scientific and geographical instruments of today are not precise enough to predict the weather in that time.'
    else:
        return 'Unfortunately, scientists do not have enough weather data to precisely gauge the weather in that time.'

# Critical Function
def form_response_weather(resp):
    """Form a response for weather based on user's interaction with chatbot.
    
    Parameters:
    resp -- response from Wit.ai
    """
    # Dealing with Location
    location = get_location(resp)
    if location == None:
        if get_last_location() != None:
            location = get_last_location()
        else:
            location = 'Singapore, Singapore'
    change_last_location(location)

    # Dealing with Datetime
    datetime = get_datetime(resp)
    if datetime == None:
        if get_last_datetime() != None:
            datetime = get_last_datetime()
        else:
            datetime = 'now'
    change_last_datetime(datetime)

    # Forming the Responses
    if datetime == 'now':
        date_dist = 0
    if datetime != 'now':
        date_dist = (int(datetime[8:10]) - __time.get_dt_now()[2])
    weather_info = weather.lookup_by_location(location)
    if weather_info == None:
        return (0, message_invalid_location())
    try:
        forecast = weather_info.forecast[date_dist].text
    except KeyError:
        return (0, message_invalid_location())
    except IndexError:
        return (0, message_too_far_ahead())
    if date_dist == 0:
        return (0, 'It is {} in {} right now.'.format(forecast, location))
    return (0, 'It will be {} in {} in {} days\'s time.'.format(forecast, location, date_dist))

# Context (Weather) Elements
last_location = []
last_datetime = []

# Context (Weather) Handlers
def clear_all_context():
    """Clear last_location and last_datetime context elements in _weather.py."""
    last_location.clear()
    last_datetime.clear()

def get_last_location():
    """Get the latest element in last_location, or returns None if empty."""
    if len(last_location) == 0:
        return None
    return last_location[len(last_location) - 1]

def get_last_datetime():
    """Get the latest element in last_datetime, or returns None if empty."""
    if len(last_datetime) == 0:
        return None
    return last_datetime[len(last_datetime) - 1]

def clear_last_location():
    """Clear last_location in _weather.py."""
    last_location.clear()

def clear_last_datetime():
    """Clear last_datetime in _weather.py."""
    last_datetime.clear()

def change_last_location(loc):
    """Update last_location based on new location from ongoing conversation with
    chatbot.
    
    Parameters:
    loc -- location from Wit.ai response
    """
    clear_last_location()
    last_location.append(loc)

def change_last_datetime(datetime):
    """Update last_datetime based on new datetime from ongoing conversation with
    chatbot.
    
    Parameters:
    datetime -- datetime stamp from Wit.ai response
    """
    clear_last_datetime()
    last_datetime.append(datetime)
