from dash import Dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from utils import (
    load_and_clean_pedestrian_data,
    year_footfalls_fig,
    sensor_counts_fig,
    sensor_footfalls_fig,
    sensor_line_fig,
)

DATA_DF = load_and_clean_pedestrian_data()


app = Dash(__name__)

app.layout = html.Div(
    id="content",
    children=[
        dcc.Graph(figure=year_footfalls_fig(DATA_DF, height=400)),
        dcc.Graph(figure=sensor_counts_fig(DATA_DF, height=400)),
#        dcc.Graph(id="sensor-footfalls", figure=sensor_footfalls_fig(DATA_DF)),
        dcc.Graph(id="sensor-footfalls", figure=sensor_line_fig(DATA_DF, height=800)),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
