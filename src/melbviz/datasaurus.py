from ipywidgets import interact, fixed, HBox, Output, Dropdown
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def object_as_widget(obj):
    out = Output()
    with out:
        display(obj)
    return out


def show_datasaurus(datasauraus_df, column):
    if column == "all":
        df = datasauraus_df
    else:
        df = datasauraus_df[datasauraus_df["dataset"] == column]
    stats_df = pd.DataFrame({
        "statistic": ["x_mean", "y_mean", "x_std", "y_std", "corr"],
        "value": [
            df["x"].mean(), df["y"].mean(), df["x"].std(), df["y"].std(), df["x"].corr(df["y"])
        ],
    })
    if column == "all":
        fig = px.scatter(datasauraus_df, facet_col_wrap=5, facet_col="dataset", x="x", y="y")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    else:
        fig = px.scatter(df, x="x", y="y")
    fig.update_layout(
        margin={"r": 10, "t": 40, "b": 10},
        font_size=18,
        width=600,
        height=500,
    )
    return HBox([object_as_widget(stats_df), go.FigureWidget(fig)])


def make_datasaurus(path="data/DatasaurusDozen.tsv"):
    datasauraus_df = pd.read_csv(path, delimiter="\t")
    columns = list(datasauraus_df["dataset"].unique())
    columns.append("all")
    widget = interact(show_datasaurus, datasauraus_df=fixed(datasauraus_df), column=columns)
    return widget
