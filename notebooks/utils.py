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


def issequence(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, collections.abc.Sequence)


def filter_foot_df(df, year=None, month=None, sensor=None):
    """Filter a pedestrian footfalls DataFrame"""
    if year is not None:
        if not issequence(year):
            year = [year]
        df = df[df["Year"].isin(set(year))]
    if month is not None:
        if not issequence(month):
            month = [month]
        df = df[df["Month"].isin(set(month))]
    if sensor is not None:
        if not issequence(sensor):
            sensor = [sensor]
        df = df[df["Sensor_Name"].isin(set(sensor))]
#    if len(df) == 0:
#        raise Exception("No matching records")
    return df


def display_output(func):
    """Decorator for displaying the result of a function in Jupyter"""
    @functools.wraps(func)
    def wrapped_display_output(*args, **kwargs):
        result = func(*args, **kwargs)
        display(result)
        return result
    return wrapped_display_output