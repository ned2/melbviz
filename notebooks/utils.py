import collections
import functools

import pandas as pd


def load_and_clean_pedestrian_data(path):
    """Load and clean the pedestrian footfall dataset into a DataFrame"""
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(
        {
            "day": df["Mdate"],
            "year": df["Year"],
            "hour": df["Time"],
            "month": pd.to_datetime(df["Month"], format="%B").dt.month,
        }
    )
    df["datetime_flat_year"] = pd.to_datetime(
        {
            "day": df["Mdate"],
            "year": 2000,
            "hour": df["Time"],
            "month": pd.to_datetime(df["Month"], format="%B").dt.month,
        }
    )
    return df


def is_sequence(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, collections.abc.Sequence)


#@functools.lru_cache()
def filter_foot_df(df, year=None, month=None, sensor=None):
    """Filter a pedestrian footfalls DataFrame"""
    if year:
        if not is_sequence(year):
            year = [year]
        df = df[df["Year"].isin(set(year))]
    if month:
        if not is_sequence(month):
            month = [month]
        df = df[df["Month"].isin(set(month))]
    if sensor:
        if not is_sequence(sensor):
            sensor = [sensor]
        df = df[df["Sensor_Name"].isin(set(sensor))]
    return df


def display_output(func):
    """Decorator for displaying the result of a function in Jupyter"""
    @functools.wraps(func)
    def wrapped_display_output(*args, **kwargs):
        result = func(*args, **kwargs)
        display(result)
        return result
    return wrapped_display_output


def geocode_sensors(df):
    """Get a DataFrame of Sensor_Name,lat,long"""
    locations_df = pd.DataFrame({"Sensor_Name":df["Sensor_Name"].unique()})
    location_strings = locations_df["Sensor_Name"] + " Melbourne, Australia"
    lat_lngs = [geocoder.google(loc, key=GOOGLE_GEO_KEY).latlng for loc in location_strings]
    lat_lngs_df = pd.DataFrame(lat_lngs, columns=['lat', 'long'])
    return pd.concat([locations_df, lat_lngs_df], axis=1)
