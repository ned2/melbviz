import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .config import MAPBOX_KEY


px.set_mapbox_access_token(MAPBOX_KEY)


def plot_sensor_counts(df, title_func=None, **kwargs):
    """Make a bar chart for total footfals for each sensor"""
    title = "Ranked Sensor Traffic"
    if callable(title_func):
        title = title_func(title)
    total_df = (
        df.groupby("Sensor_Name")["Hourly_Counts"]
        .sum()
        .sort_values()
        .reset_index(name="Total Counts")
    )
    if "height" not in kwargs:
        kwargs["height"] = max(18 * len(total_df), 500)

    figure = px.bar(
        total_df,
        x="Total Counts",
        y="Sensor_Name",
        orientation="h",
        title=title,
        **kwargs,
    )
    figure.update_layout(
        title_x=0.5,
        yaxis_title=None,
        yaxis_showgrid=False,
        xaxis_title=None,
        xaxis_side="top",
    )
    return figure


def plot_month_counts(df, split_sensors=False, title_func=None, **kwargs):
    title = f"Monthly Sensor Traffic"
    if callable(title_func):
        title = title_func(title)
    if split_sensors:
        group_cols = ["Month", "Sensor_Name"]
        color = "Sensor_Name"
    else:
        group_cols = ["Month"]
        color = None
    month_df = df.groupby(group_cols)["Hourly_Counts"].sum().reset_index()
    month_df["month_num"] = pd.to_datetime(month_df.Month, format="%B").dt.month
    figure = px.bar(
        month_df.sort_values(by="month_num"),
        x="Month",
        y="Hourly_Counts",
        barmode="group",
        color=color,
        title=title,
        **kwargs,
    )
    figure.update_layout(
        title_x=0.5,
        yaxis_title="Total Counts",
        yaxis_showgrid=False,
        yaxis_zeroline=False,
        xaxis_title=None,
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            xanchor="right",
            x=1,
        ),
    )
    return figure


def plot_sensor_traffic(
    df, same_yscale=False, row_height=150, limit=5, title_func=None, **kwargs,
):
    if len(df) == 0:
        return None
    title = f"Hourly Pedestrian Traffic by Sensor"
    if callable(title_func):
        title = title_func(title)
    target_sensors = (
        df.groupby("Sensor_Name")["Hourly_Counts"].sum().sort_values(ascending=False)
    )[:limit]

    df = df[df["Sensor_Name"].isin(set(target_sensors.index))]

    if "height" not in kwargs:
        kwargs["height"] = max(len(target_sensors) * row_height, 400)

    figure = px.line(
        df,
        y="Hourly_Counts",
        x="datetime",
        facet_row="Sensor_Name",
        title=title,
        category_orders={"Sensor_Name": list(target_sensors.index)},
        **kwargs,
    )
    figure.update_layout(title_x=0.5)
    figure.update_yaxes(
        matches=None if same_yscale else "y",
        showgrid=False,
        zeroline=False,
        title_text=None,
    )
    figure.update_xaxes(showgrid=True, title_text=None)
    figure.for_each_annotation(
        lambda a: a.update(x=0.5, textangle=0, text=a.text.split("=")[-1])
    )
    return figure


def plot_year_traffic(df, same_yscale=False, row_height=150, title_func=None, **kwargs):
    """Plot traffic for a single sensor
    Note: assumes the DataFrame has been filtered to a single sensor already. 
    """
    if len(df) == 0:
        return None
    sensor = df["Sensor_Name"].unique()[0]
    title = f"{sensor} Hourly Footfall Counts by year"
    if callable(title_func):
        title = title_func(title)
    year_counts = df.groupby("Year")["Hourly_Counts"].sum().sort_index(ascending=False)

    if "height" not in kwargs:
        kwargs["height"] = max(len(year_counts) * row_height, 500)

    # make the figure with Plotly Express
    figure = px.line(
        df,
        y="Hourly_Counts",
        x="datetime_flat_year",
        facet_row="Year",
        title=title,
        category_orders={"Year": list(year_counts.index)},
        **kwargs,
    )

    # update figure produced by Plotly Express with fine-tuning
    figure.update_yaxes(
        matches=None if same_yscale else "y",
        showgrid=False,
        zeroline=False,
        title_text=None,
    )
    figure.update_xaxes(showgrid=True, title_text=None)
    figure.for_each_annotation(
        lambda a: a.update(textangle=0, text=a.text.split("=")[-1])
    )
    figure.update_layout(title_x=0.5)
    return figure


def plot_sensor_map(df, title_func=None, **kwargs):
    title = "Sensor Traffic"
    if callable(title_func):
        title = title_func(title)
    sensor_totals_df = (
        df.groupby("Sensor_Name")
        .agg(
            {
                "Hourly_Counts": sum,
                "latitude": lambda x: x.iloc[0],
                "longitude": lambda x: x.iloc[0],
            }
        )
        .reset_index().rename(columns={"Hourly_Counts": "Total Counts"})
    )
    figure = px.scatter_mapbox(
        sensor_totals_df,
        lat="latitude",
        lon="longitude",
        color="Total Counts",
        size="Total Counts",
        text="Sensor_Name",
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=50,
        zoom=13,
        title=title,
        **kwargs,
    )
    figure.update_layout(title_x=0.5,)
    return figure


def plot_stacked_sensors(df, year=None, sensor=None, normalised=True, title_func=None):
    title = "Proportion of footfalls for each sensor by year"
    if callable(title_func):
        title = title_func(title)
    sensor_years_s = df.groupby(["Sensor_Name", "Year"])["Hourly_Counts"].sum()
    sensor_dfs = [
        (sensor, dfx.reset_index("Sensor_Name"))
        for sensor, dfx in sensor_years_s.groupby(level=0)
    ]

    figure = go.Figure()
    for sensor, df in sensor_dfs:
        figure.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Hourly_Counts"],
                # mode='lines',
                name=sensor,
                stackgroup="one",
                groupnorm="percent" if normalised else "",
            )
        )

    figure.update_layout(width=1500, height=1200, title=title)
    return figure
