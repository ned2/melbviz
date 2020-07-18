import calendar
import functools
import numbers

import pandas as pd


def display_output(func):
    """Decorator for displaying the result of a function in Jupyter"""

    @functools.wraps(func)
    def wrapped_display_output(*args, **kwargs):
        result = func(*args, **kwargs)
        display(result)
        return result

    return wrapped_display_output


def sort_months(months):
    """Sort a sequence of months by their calendar order"""
    month_ref = list(calendar.month_name)[1:]
    return sorted(months, key=lambda month: month_ref.index(month))


def is_value(obj):
    """Check if an object is a string or numeric value"""
    return isinstance(obj, str) or isinstance(obj, numbers.Number)


def geocode_sensors(df):
    """Get a DataFrame of Sensor_Name,lat,long
    
    This is done by appending "Melbourne, Australia" to sensor names and sending
    these location strings to Google Geocoding API to be geocoded.

    Note: Melbourne City Council provides a separate dataset of sensor locations
    so this is probably not needed.
    """
    locations_df = pd.DataFrame({"Sensor_Name": df["Sensor_Name"].unique()})
    location_strings = locations_df["Sensor_Name"] + " Melbourne, Australia"
    lat_lngs = [
        geocoder.google(loc, key=GOOGLE_GEO_KEY).latlng for loc in location_strings
    ]
    lat_lngs_df = pd.DataFrame(lat_lngs, columns=["lat", "long"])
    return pd.concat([locations_df, lat_lngs_df], axis=1)
