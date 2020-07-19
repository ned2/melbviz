import collections
from functools import lru_cache, cached_property

from IPython.display import display
import pandas as pd

from .utils import display_output, is_value, sort_months
from .plots import (
    plot_sensor_counts,
    plot_month_counts,
    plot_sensor_traffic,
    plot_year_traffic,
    plot_sensor_map,
    plot_stacked_sensors,
)


class PedestrianDataset:

    plot_func_map = {
        "sensor_counts": plot_sensor_counts,
        "month_counts": plot_month_counts,
        "sensor_traffic": plot_sensor_traffic,
        "year_traffic": plot_year_traffic,
        "sensor_map": plot_sensor_map,
        "stacked_sensors": plot_stacked_sensors,
    }

    def __init__(self, dataframe, filters=None, debug=False):
        self._dataframe = dataframe
        self.debug = debug

    @property
    def df(self):
        return self._dataframe

    @cached_property
    def years(self):
        return sorted(self.df["Year"].unique())

    @cached_property
    def months(self):
        return sort_months(self.df["Month"].unique())

    @cached_property
    def sensors(self):
        return sorted(self.df["Sensor_Name"].unique())

    @classmethod
    def load(cls, csv_path, sensor_csv_path=None, **kwargs):
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

        if sensor_csv_path is not None:
            geo_df = pd.read_csv(sensor_csv_path)
            df = df.merge(geo_df, left_on="Sensor_Name", right_on="sensor_description")
        return cls(df, **kwargs)

    @lru_cache()
    def filter(self, year=None, month=None, sensor=None):
        """Filter the dataset dataset.
        
        Returns a filtered instance of a FootDataset
        """
        df = self.df
        params = {"Year": year, "Sensor_Name": sensor, "Month": month}
        if self.debug:
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
        return self.__class__(df, debug=self.debug)

    @classmethod
    def get_plot_func(cls, kind):
        if kind not in cls.plot_func_map:
            kinds = ", ".join(f"'{plot}'" for plot in cls.plot_func_map.keys())
            msg = f"'{kind}' is not a valid plot type. Available plots are:\n\n{kinds}"
            raise ValueError()
        return cls.plot_func_map[kind]

    def get_fig(self, plot_kind, *args, **kwargs):
        """Get Plotly Figure from a range of custom figures"""
        plot_func = self.get_plot_func(plot_kind)
        return plot_func(self.df, *args, **kwargs)

    def plot(self, *args, **kwargs):
        """Plot and display a Figure in a notebook"""
        figure = self.get_fig(*args, **kwargs)
        return display(figure)
