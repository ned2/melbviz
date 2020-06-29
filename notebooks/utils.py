import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import config


def load_and_clean_pedestrian_data(path=config.PEDESTRIAN_DATA_PATH):
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
    return df


def sensor_footfalls_fig(df, year=None):
    """Make a vertical bar chart for total footfalls for each sensor"""
    title = "Total footfalls by sensor"
    if year is not None:
        df = df[df["Year"] == year]
        title = title + f" for {year}"
    total = df.groupby("Sensor_Name")["Hourly_Counts"].sum().sort_values()
    fig = px.bar(
        y=total.index, x=total, title=title, orientation="h", height=1800, width=1000
    ).update_layout(title_x=0.5)
    return fig


def year_footfalls_fig(df, height=None, width=None):
    """Make a plot of total footfalls for each year"""
    year_counts = df.groupby("Year")["Hourly_Counts"].sum()
    fig = (
        px.line(
            x=year_counts.index,
            y=year_counts,
            title="Total Footfalls by Year",
            labels={"x": "Year", "y": "Footfalls"},
            height=height,
            width=width,
        )
        .update_traces(mode="lines+markers")
        .update_layout(title_x=0.5)
    )
    return fig


def sensor_counts_fig(df, height=None, width=None):
    """Make a plot of number of sensors by year"""
    num_sensors = df.groupby("Year")["Sensor_Name"].nunique()
    fig = (
        px.line(
            x=num_sensors.index,
            y=num_sensors,
            title="Number sensors by year",
            labels={"x": "Year", "y": "Number of Sensors"},
            height=height,
            width=width,
        )
        .update_traces(mode="lines+markers")
        .update_layout(title_x=0.5)
    )
    return fig


def sensor_line_fig(df, years=None, sensors=None, normalised=True, height=None, width=None):
    """Make line plot of footfalls for each sensor"""
    if years is not None:
        df = df[df["Year"].isin(years)]
    if sensors is not None:
        df = df[df["Sensor_Name"].isin(sensors)]
    sensor_years_s = df.groupby(["Sensor_Name", "Year"])["Hourly_Counts"].sum()
    sensor_dfs = [
        (sensor, dfx.reset_index("Sensor_Name"))
        for sensor, dfx in sensor_years_s.groupby(level=0)
    ]

    fig = go.Figure()
    for sensor, df in sensor_dfs:
        fig.add_trace(
            go.Scatter(
                mode="lines+markers",
                x=df.index,
                y=df["Hourly_Counts"],
                name=sensor,
                hovertemplate="%{y:,}",
                # don't truncate the hover text
                hoverlabel={"namelength": -1},
                # line=go.scatter.Line(color="gray"),
            )
        )

    fig.update_layout(
        clickmode="event+select",
        width=width,
        height=height,
        title="Proportion of footfalls for each sensor by year",
    )
    return fig
