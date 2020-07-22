import calendar
import collections
import functools
import numbers

import pandas as pd


def load_and_clean_pedestrian_data(counts_csv_path, sensor_csv_path=None):
    df = pd.read_csv(counts_csv_path).set_index("ID")
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
    if sensor_csv_path is not None:
        geo_df = pd.read_csv(sensor_csv_path)
        df = df.merge(geo_df, left_on="Sensor_Name", right_on="sensor_description")
    df = df.sort_values("datetime")
    return df


def filter_pedestrian_df(df, year=None, month=None, sensor=None, debug=False):
    params = {"Year": year, "Sensor_Name": sensor, "Month": month}
    if debug:
        print(f"Filter params: {params}")
    for param, param_val in params.items():
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


def sort_months(months):
    """Sort a sequence of months by their calendar order"""
    month_ref = list(calendar.month_name)[1:]
    return sorted(months, key=lambda month: month_ref.index(month))


def title_with_filters(title, filters=None):
    if filters is None:
        return title
    filter_vals = [
        filters[param] for param in ["month", "year"] if filters.get(param, None)
    ]
    if len(filter_vals) == 0:
        return title
    suffix = ", ".join(str(f_val) for f_val in filter_vals)
    return f"{title} for {suffix}"


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


def make_options(sequence):
    return [{"label": item, "value": item} for item in sequence]
