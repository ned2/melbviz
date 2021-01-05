from functools import cached_property, lru_cache, partial

from IPython.display import display
import pandas as pd

from . import plots
from .config import COUNTS_CSV_PATH, SENSOR_CSV_PATH, CLEANED_DATA_PATH
from .utils import (
    sort_months,
    filter_pedestrian_df,
    load_and_clean_pedestrian_data,
    title_with_filters,
)

class PedestrianDataset:

    plot_func_map = {
        "sensor_counts": plots.plot_sensor_counts,
        "month_counts": plots.plot_month_counts,
        "sensor_traffic": plots.plot_sensor_traffic,
        "year_traffic": plots.plot_year_traffic,
        "sensor_map": plots.plot_sensor_map,
        "stacked_sensors": plots.plot_stacked_sensors,
    }

    def __init__(self, df, figure_layout=None, cache=True, debug=False):
        self.params = {}
        self.active_filters = {}
        self.df = df
        self.params["cache"] = cache
        self.params["debug"] = debug
        if figure_layout is None:
            figure_layout = {}
        self.params["figure_layout"] = figure_layout

    @property
    def df(self):
        """Pandas DataFrame containing data for this dataset."""
        return self._dataframe

    @df.setter
    def df(self, df):
        self._dataframe = df

    @property
    def available_plots(self):
        return list(self.plot_func_map.keys())

    @cached_property
    def years(self):
        """Sorted list of years present in this dataset"""
        return sorted(self.df["Year"].unique())

    @cached_property
    def months(self):
        """Sorted list of months present in this dataset"""
        return sort_months(self.df["Month"].unique())

    @cached_property
    def sensors(self):
        """Alphabetically sorted list of months present in this dataset"""
        return sorted(self.df["Sensor_Name"].unique())

    @classmethod
    def load(cls, counts_csv_path=COUNTS_CSV_PATH, sensor_csv_path=SENSOR_CSV_PATH, **kwargs):
        """Load and clean the pedestrian dataset into a DataFrame"""
        df = load_and_clean_pedestrian_data(counts_csv_path, sensor_csv_path)
        return cls(df, **kwargs)

    @classmethod
    def from_parquet(cls, path=CLEANED_DATA_PATH, **kwargs):
        """Load a dataset from a saved Parquet file."""
        df = pd.read_parquet(path)
        return cls(df, **kwargs)

    @classmethod
    def from_csv(cls, path, **kwargs):
        """Load a dataset from a cleaned and saved CSV file."""
        df = pd.read_csv(path, parse_dates=["datetime", "datetime_flat_year"])
        return cls(df, **kwargs)

    def to_parquet(self, path=CLEANED_DATA_PATH):
        """Write the DataFrame to disk as Parquet using standardised config."""
        self.df.to_parquet(path, engine="fastparquet", compression="gzip")

    def to_csv(self, path, **kwargs):
        """Write the DataFrame to disk as CSV"""
        self.df.to_csv(path, **kwargs)

    def filter(self, year=None, month=None, sensor=None):
        """Filter this dataset dataset, returning new PedestrianDataset instance"""
        if self.params["cache"]:
            filter_func = self._filter_df_cached
            # arguments to functions decorated by `lru_cache`` must be hashable
            if isinstance(year, list):
                year = tuple(year)
            if isinstance(month, list):
                month = tuple(month)
            if isinstance(sensor, list):
                sensor = tuple(sensor)
        else:
            filter_func = self._filter_df
        filters = {"year": year, "month": month, "sensor": sensor}
        df = filter_func(**filters)
        new_dataset = self.__class__(df, **self.params)
        new_dataset.active_filters = filters
        return new_dataset

    def _filter_df(self, year=None, month=None, sensor=None):
        return filter_pedestrian_df(
            self.df, year=year, month=month, sensor=sensor, debug=self.params["debug"]
        )

    @lru_cache()
    def _filter_df_cached(self, year=None, month=None, sensor=None):
        return filter_pedestrian_df(
            self.df, year=year, month=month, sensor=sensor, debug=self.params["debug"]
        )

    @classmethod
    def get_plot_func(cls, kind):
        if kind not in cls.plot_func_map:
            kinds = ", ".join(f"'{plot}'" for plot in cls.plot_func_map.keys())
            msg = f"'{kind}' is not a valid plot type. Available plots are:\n\n{kinds}"
            raise ValueError()
        return cls.plot_func_map[kind]

    def get_fig(self, plot_kind, title_filters=True, **kwargs):
        """Make a Plotly Figure from a range of custom figures

        plot_kind     The name of the type of figure to generate.
        title_filters Boolean indicates whether to add active filters to title.
        **kwargs      Keyword arguments will be passed into the  
                      keyword arguments of the underling Plotly Express call.
        """
        if title_filters:
            title_func = partial(title_with_filters, filters=self.active_filters)
        else:
            title_func = None
        plot_func = self.get_plot_func(plot_kind)
        figure = plot_func(self.df, title_func=title_func, **kwargs)
        if figure is not None:
            # TODO: need better solution for when plotting empty DataFrame
            figure.update_layout(**self.params["figure_layout"])
        return figure

    def plot(self, *args, **kwargs):
        """Make and display a Plotly Figure in a notebook"""
        figure = self.get_fig(*args, **kwargs)
        return display(figure)
