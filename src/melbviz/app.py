from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .pedestrian import PedestrianDataset
from .config import DATA_PATH
from .utils import make_options


app = Dash(__name__)
data = PedestrianDataset.from_parquet(DATA_PATH / "melbviz_small.parquet")


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
            [html.Label("Sensor"), dcc.Dropdown(id="sensor-input", className="input")]
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
                    figure=data.get_fig("month_counts"),
                    config={"displayModeBar": False},
                ),
            ],
        ),
    ],
)


content = html.Div(
    id="content",
    children=[
        dcc.Graph(id="sensor-map", config={"displayModeBar": False}),
        dcc.Graph(id="sensor-counts", config={"displayModeBar": False}),
        dcc.Graph(id="sensor-traffic", config={"displayModeBar": False}),
    ],
)


app.layout = html.Div([sidebar, content])


@app.callback(
    [Output("month-input", "options"), Output("sensor-input", "options")],
    [Input("year-input", "value")],
)
def update_inputs(year):
    new_data = data.filter(year)
    return (make_options(new_data.months), make_options(new_data.sensors))


@app.callback(
    Output("sensor-map", "figure"),
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("sensor-input", "value"),
    ],
)
def sensor_map(year, month, sensor):
    return data.filter(year=year, month=month, sensor=sensor).get_fig("sensor_map")


@app.callback(
    Output("month-counts", "figure"),
    [Input("year-input", "value"), Input("sensor-input", "value"),],
)
def month_counts(year, sensor):
    return data.filter(year=year, sensor=sensor).get_fig("month_counts")


@app.callback(
    Output("sensor-counts", "figure"),
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("sensor-input", "value"),
    ],
)
def sensor_counts(year, month, sensor):
    return data.filter(year=year, month=month, sensor=sensor).get_fig("sensor_counts")


@app.callback(
    Output("sensor-traffic", "figure"),
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("sensor-input", "value"),
    ],
)
def sensor_traffic(year, month, sensor):
    return data.filter(year, month, sensor).get_fig("sensor_traffic")
