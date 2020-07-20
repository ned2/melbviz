from functools import lru_cache, cached_property

from IPython.display import display
import pandas as pd

from .utils import sort_months, filter_pedestrian_df, load_and_clean_pedestrian_data
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

    def write_parquet(self, path):
        """Write a PandasFrame to disk as Parquet using standardised config."""
        self.df.to_parquet(path, engine="fastparquet", compression="snappy")

    @classmethod
    def load(cls, counts_csv_path, sensor_csv_path=None, **kwargs):
        """Load and clean the pedestrian dataset into a DataFrame"""
        df = load_and_clean_pedestrian_data(counts_csv_path, sensor_csv_path)
        return cls(df, **kwargs)

    @classmethod
    def from_parquet(cls, path, **kwargs):
        """Write a PandasFrame to disk as Parquet using standardised config."""
        df = pd.read_parquet(path)
        return cls(df, **kwargs)
        
    @lru_cache()
    def filter(self, year=None, month=None, sensor=None):
        """Filter the dataset dataset, returning new instance of a PedestrianDataset"""
        df = filter_pedestrian_df(
            self.df, year=year, month=month, sensor=sensor, debug=self.debug
        )
        return self.__class__(df, debug=self.debug)

    @classmethod
    def get_plot_func(cls, kind):
        if kind not in cls.plot_func_map:
            kinds = ", ".join(f"'{plot}'" for plot in cls.plot_func_map.keys())
            msg = f"'{kind}' is not a valid plot type. Available plots are:\n\n{kinds}"
            raise ValueError()
        return cls.plot_func_map[kind]

    def get_fig(self, plot_kind, *args, **kwargs):
        """Make a Plotly Figure from a range of custom figures"""
        plot_func = self.get_plot_func(plot_kind)
        return plot_func(self.df, *args, **kwargs)

    def plot(self, *args, **kwargs):
        """Make and display a Plotly Figure in a notebook"""
        figure = self.get_fig(*args, **kwargs)
        return display(figure)
