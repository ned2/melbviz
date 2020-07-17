import functools
import numbers

import pandas as pd


class PedestrianDataset:
    
    def __init__(self, df):
        self.df = df
    
    @classmethod
    def load(cls, csv_path, lat_long_path=None):
        """Load and clean the pedestrian dataset into a DataFrame"""
        df = pd.read_csv(csv_path)
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
        return cls(df)
    
    @functools.lru_cache()
    def filter(self, year=None, month=None, sensor=None):
        """Filter the dataset dataset.
        
        Returns a filtered instance of a FootDataset
        """
        df = self.df
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
            df = self.df[self.df[param].isin(set(param_val))]
        return self.__class__(df)

    def plot(self, type):
        # this needs to:
        # A: recieve a ploit 
        pass


def is_value(obj):
    return isinstance(obj, str) or isinstance(obj, numbers.Number)
