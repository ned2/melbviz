import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import MAPBOX_KEY
from utils import filter_foot_df, is_value


px.set_mapbox_access_token(MAPBOX_KEY)


def plot_sensor_counts(df, year=None, month=None, sensor=None, **kwargs):
    """Make a bar chart for total footfals for each sensor"""
    df = filter_foot_df(df, year=year, month=month, sensor=sensor)
    total_df = (
        df.groupby("Sensor_Name")["Hourly_Counts"]
        .sum()
        .sort_values()
        .reset_index(name="Total Counts")
    )
    kwargs["height"] = 18 * len(total_df)
    fig = px.bar(
        total_df, x="Total Counts", y="Sensor_Name", orientation="h", **kwargs,
    )
    fig.update_layout(yaxis_title=None, xaxis_side="top")
    return fig


def plot_month_counts(df, year=None, sensor=None, **kwargs):
    df = filter_foot_df(df, year=year, sensor=sensor)
    if not is_value(sensor) and len(sensor) > 1:
        group_cols = ["Month", "Sensor_Name"]
        color = "Sensor_Name"
    else:
        group_cols = ["Month"]
        color = None
    month_df = df.groupby(group_cols)["Hourly_Counts"].sum().reset_index()
    month_df["month_num"] = pd.to_datetime(month_df.Month, format="%B").dt.month
    fig = px.bar(
        month_df.sort_values(by="month_num"),
        x="Month",
        y="Hourly_Counts",
        barmode="group",
        color=color,
        **kwargs,
    )
    fig.update_layout(yaxis_title="Total Counts", xaxis_title=None)
    return fig


def plot_sensors(
    df,
    sensor=None,
    year=None,
    month=None,
    same_yscale=False,
    row_height=150,
    limit=10,
    **kwargs,
):
    if not isinstance(sensor, str):
        # Too many plots doesn't make sense visually and also plotly express
        # does not like it.
        sensor = list(sensor)[:limit]

    df = filter_foot_df(df, year=year, month=month, sensor=sensor)
    if len(df) == 0:
        return None

    title = f"Hourly Footfall Counts by Sensor"
    title_filters = [str(fil) for fil in (month, year) if fil is not None]
    if title_filters:
        title += f" for {' '.join(title_filters)}"

    target_sensors = (
        df.groupby("Sensor_Name")["Hourly_Counts"].sum().sort_values(ascending=False)
    )[:limit]
    df = filter_foot_df(df, sensor=target_sensors.index)

    fig = px.line(
        df,
        y="Hourly_Counts",
        x="datetime",
        facet_row="Sensor_Name",
        title=title,
        category_orders={"Sensor_Name": list(target_sensors.index)},
        height=len(target_sensors) * row_height,
        **kwargs,
    )

    fig.update_yaxes(
        matches=None if same_yscale else "y",
        showgrid=False,
        zeroline=False,
        title_text=None,
    )
    fig.update_xaxes(showgrid=True, title_text=None)
    fig.for_each_annotation(lambda a: a.update(textangle=0, text=a.text.split("=")[-1]))
    fig.update_layout(title_x=0.5)
    return fig


def plot_years(
    df, sensor=None, year=None, month=None, same_yscale=False, row_height=100, **kwargs
):
    df = filter_foot_df(df, year=year, month=month, sensor=sensor)
    if len(df) == 0:
        return None

    title = f"{sensor} Hourly Footfall Counts by year"
    if month is not None:
        title += f" for {month}"

    # prep additional data required
    year_counts = df.groupby("Year")["Hourly_Counts"].sum().sort_index(ascending=False)

    # make the figure with Plotly Express
    fig = px.line(
        df,
        y="Hourly_Counts",
        x="datetime_flat_year",
        facet_row="Year",
        title=title,
        category_orders={"Year": list(year_counts.index)},
        height=len(year_counts) * row_height,
        **kwargs,
    )

    # update figure produced by Plotly Express with fine-tuning
    fig.update_yaxes(
        matches=None if same_yscale else "y",
        showgrid=False,
        zeroline=False,
        title_text=None,
    )
    fig.update_xaxes(showgrid=True, title_text=None)
    fig.for_each_annotation(lambda a: a.update(textangle=0, text=a.text.split("=")[-1]))
    fig.update_layout(title_x=0.5)
    return fig


def plot_scatter_map(df, year=None, month=None, sensor=None, **kwargs):
    df = filter_foot_df(df, year=year, month=None, sensor=sensor)
    sensor_totals_df = (
        df.groupby("Sensor_Name")
        .agg(
            {
                "Hourly_Counts": sum,
                "latitude": lambda x: x.iloc[0],
                "longitude": lambda x: x.iloc[0],
            }
        )
        .reset_index()
    )
    return px.scatter_mapbox(
        sensor_totals_df,
        lat="latitude",
        lon="longitude",
        # color="peak_hour",
        size="Hourly_Counts",
        text="Sensor_Name",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=20,
        zoom=13,
        **kwargs,
    )


def plot_stacked_sensors(df, year=None, sensor=None, normalised=True):
    df = filter_foot_df(df, year=year, sensor=sensor)
    sensor_years_s = df.groupby(["Sensor_Name", "Year"])["Hourly_Counts"].sum()
    sensor_dfs = [
        (sensor, dfx.reset_index("Sensor_Name"))
        for sensor, dfx in sensor_years_s.groupby(level=0)
    ]

    fig = go.Figure()
    for sensor, df in sensor_dfs:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Hourly_Counts"],
                # mode='lines',
                name=sensor,
                stackgroup="one",
                groupnorm="percent" if normalised else "",
            )
        )

    fig.update_layout(
        width=1500, height=1200, title="Proportion of footfalls for each sensor by year"
    )
    return fig


# don't think we need this
def make_line_plot(df, years=None, sensors=None, normalised=True):
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
        width=1500,
        height=1000,
        title="Proportion of footfalls for each sensor by year",
    )
    return fig
