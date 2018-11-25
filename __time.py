"""
Extension of main.py and weather.py for processing date and time
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
"""

from datetime import datetime

# Function that returns date and time
def get_dt_now():
    """Get the current date and time and returns a list containing, in sequence,
    the year, month, day, hour, minute and second.
    """
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    return [year, month, day, hour, minute, second]
