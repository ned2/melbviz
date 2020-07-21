from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from melbviz.pedestrian import PedestrianDataset
from melbviz.config import DATA_PATH


data = PedestrianDataset.from_parquet(DATA_PATH / "melbviz_small.parquet")

app = Dash(__name__)


controls = html.Div(
    id="controls",
    children=[
        html.Div([html.Label("Year"), dcc.Dropdown(id="year-input")]),
        html.Div([html.Label("Month"), dcc.Dropdown(id="month-input")]),
        html.Div([html.Label("Sensor"), dcc.Dropdown(id="sensor-input")]),
    ],
)


app.layout = html.Div(
    [
        html.Div(
            id="sidebar",
            children=[
                html.H1("Melbourne CBD Pedestrian Traffic"),
                html.Div(
                    id="controls-months",
                    children=[controls, dcc.Graph(figure=data.get_fig("month_counts"))],
                ),
            ],
        ),
        html.Div(
            id="content",
            children=[
                dcc.Graph(
                    id="sensor-map",
                    figure=data.get_fig("sensor_map"),
                    config={"displayModeBar": False},
                ),
                dcc.Graph(
                    id="sensor-counts",
                    figure=data.get_fig("sensor_counts"),
                    config={"displayModeBar": False},
                ),
                dcc.Graph(
                    id="sensor-traffic",
                    figure=data.get_fig("sensor_traffic"),
                    config={"displayModeBar": False},
                ),
            ],
        ),
    ]
)
