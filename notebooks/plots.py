import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import filter_foot_df


def plot_sensor_counts(df, year=None, month=None):
    """Make a bar chart for total footfals for each sensor"""
    df = filter_foot_df(df, year=year)
    title = "Total footfalls by sensor"
    total = df.groupby("Sensor_Name")["Hourly_Counts"].sum().sort_values()
    return px.bar(y=total.index, x=total, title=title, orientation='h', height=2000, width=1000)


def plot_month_counts(df, year=None, sensor=None):
    df = filter_foot_df(df, year=year, sensor=sensor)
    if sensor is None:
        group_cols = ["Month"]
        color = None
    else:
        group_cols = ["Month", "Sensor_Name"]
        color = "Sensor_Name"
    month_df = df.groupby(group_cols)["Hourly_Counts"].sum().reset_index()
    month_df["month_num"] = pd.to_datetime(month_df.Month, format="%B").dt.month
    return px.bar(
        month_df.sort_values(by="month_num"),
        x="Month",
        y="Hourly_Counts",
        barmode="group",
        color=color,
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


def plot_sensors(
    df, sensor=None, year=None, month=None, same_yscale=False, row_height=100, **kwargs
):
    df = filter_foot_df(df, year=year, month=month, sensor=sensor)
    if len(df) == 0:
        return None

    title = f"Hourly Footfall Counts by Sensor"
    if month or year:
        title += f" for {' '.join([month, str(year)])}"

    sensor_order = (
        df.groupby("Sensor_Name")["Hourly_Counts"].sum().sort_values(ascending=False)
    )

    # make the figure with Plotly Express
    fig = px.line(
        df,
        y="Hourly_Counts",
        x="datetime",
        facet_row="Sensor_Name",
        title=title,
        category_orders={"Sensor_Name": list(sensor_order.index)},
        height=len(sensor_order) * row_height,
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
        **kwargs
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


# don't think we need this
def make_line_plot(df, years=None, sensors=None, normalised=True):
    if years is not None:
        df = df[df["Year"].isin(years)]
    if sensors is not None:
        df = df[df["Sensor_Name"].isin(sensors)]
    sensor_years_s = df.groupby(["Sensor_Name", "Year"])["Hourly_Counts"].sum()
    sensor_dfs = [(sensor, dfx.reset_index("Sensor_Name")) for sensor, dfx in sensor_years_s.groupby(level=0)]

    fig = go.Figure()
    for sensor, df in sensor_dfs:   
        fig.add_trace(go.Scatter(
            mode="lines+markers",
            x=df.index, y=df["Hourly_Counts"],
            name=sensor,
            hovertemplate = "%{y:,}",
            # don't truncate the hover text
            hoverlabel={"namelength":-1},
            #line=go.scatter.Line(color="gray"),
        ))

    fig.update_layout(clickmode="event+select", width=1500, height=1000, title="Proportion of footfalls for each sensor by year")
    #fig.update_yaxes(hoverformat=".2")
    return fig
