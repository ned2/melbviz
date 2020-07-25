from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .pedestrian import PedestrianDataset
from .config import DATA_PATH
from .utils import make_options
from . import figure_layouts as layouts


app = Dash(__name__)

# this will be passed into the layout of each figure
figure_layout = dict(margin=dict(l=10, r=10, t=70, b=None, pad=None))

data = PedestrianDataset.from_parquet(
    DATA_PATH / "melbviz_small.parquet", figure_layout=figure_layout
)


controls = html.Div(
    id="controls",
    children=[
        html.Div(
            [
                html.Label("Year"),
                dcc.Dropdown(
                    id="year-input",
                    className="input",
                    options=make_options(data.years),
                    value=data.years[-1],
                ),
            ]
        ),
        html.Div(
            [html.Label("Month"), dcc.Dropdown(id="month-input", className="input")]
        ),
        html.Div(
            [
                html.Label("Sensor"),
                dcc.Dropdown(id="sensor-input", multi=True, className="input"),
            ]
        ),
    ],
)


sidebar = html.Div(
    id="sidebar",
    children=[
        html.H1("Melbourne CBD Pedestrian Traffic"),
        html.Div(
            id="controls-months",
            children=[
                controls,
                dcc.Graph(
                    id="month-counts",
                    className="loader",
                    config={"displayModeBar": False},
                ),
            ],
        ),
    ],
)


content = html.Div(
    id="content",
    children=[
        dcc.Graph(
            id="sensor-map", className="loader", config={"displayModeBar": False}
        ),
        dcc.Graph(
            id="sensor-counts", className="loader", config={"displayModeBar": False}
        ),
        dcc.Graph(
            id="sensor-traffic", className="loader", config={"displayModeBar": False}
        ),
    ],
)


app.layout = html.Div([sidebar, content])


@app.callback(
    [
        Output("month-input", "options"),
        Output("month-input", "value"),
        Output("sensor-input", "options"),
        Output("sensor-input", "value"),
    ],
    [Input("year-input", "value")],
)
def update_inputs(year):
    new_data = data.filter(year)
    return (make_options(new_data.months), None, make_options(new_data.sensors), None)


@app.callback(
    Output("month-counts", "figure"),
    [Input("year-input", "value"), Input("sensor-input", "value"),],
)
def month_counts(year, sensor):
    split_sensors = sensor is not None and len(sensor) > 1
    figure = data.filter(year=year, sensor=sensor).get_fig(
        "month_counts", split_sensors=split_sensors
    )
    figure.update_layout(layouts.clean_layout)
    return figure


@app.callback(
    Output("sensor-map", "figure"),
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("sensor-input", "value"),
    ],
)
def sensor_map(year, month, sensor):
    figure = data.filter(year=year, month=month, sensor=sensor).get_fig(
        "sensor_map", height=600
    )
    return figure


@app.callback(
    Output("sensor-counts", "figure"),
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("sensor-input", "value"),
    ],
)
def sensor_counts(year, month, sensor):

    figure = data.filter(year=year, month=month, sensor=sensor).get_fig(
        "sensor_counts", width=500
    )
    figure.update_layout(layouts.clean_layout)
    return figure


@app.callback(
    Output("sensor-traffic", "figure"),
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("sensor-input", "value"),
    ],
)
def sensor_traffic(year, month, sensor):
    figure = data.filter(year, month, sensor).get_fig("sensor_traffic")
    return figure
