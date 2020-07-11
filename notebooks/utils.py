import collections
import functools
import numbers

import pandas as pd


def load_and_clean_pedestrian_data(path, lat_long_path=None):
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

    if lat_long_path is not None:
        geo_df = pd.read_csv(lat_long_path)
        df = df.merge(geo_df, left_on="Sensor_Name", right_on="sensor_description")
    return df


def is_value(obj):
    return isinstance(obj, str) or isinstance(obj, numbers.Number)


def filter_foot_df(df, year=None, month=None, sensor=None):
    """Filter a pedestrian footfalls DataFrame"""
    param_map = {"Year": year, "Sensor_Name": sensor, "Month": month}
    for param, param_val in param_map.items():
        if param_val is None:
            continue
        elif is_value(param_val):
            param_val = [param_val]
        elif isinstance(param_val, collections.abc.Iterable):
            param_val = list(param_val)
        else:
            raise Exception(
                f"Invalid value {param_val}, params must be str, numeric, or"
                " an iterable"
            )
        if len(param_val) == 0:
            continue
        df = df[df[param].isin(set(param_val))]
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
    """Get a DataFrame of Sensor_Name,lat,long
    
    This is done by appending "Melbourne, Australia" to sensor names and sending
    these location strings to Google Geocoding API to be geocoded.
    """
    locations_df = pd.DataFrame({"Sensor_Name": df["Sensor_Name"].unique()})
    location_strings = locations_df["Sensor_Name"] + " Melbourne, Australia"
    lat_lngs = [
        geocoder.google(loc, key=GOOGLE_GEO_KEY).latlng for loc in location_strings
    ]
    lat_lngs_df = pd.DataFrame(lat_lngs, columns=["lat", "long"])
    return pd.concat([locations_df, lat_lngs_df], axis=1)
