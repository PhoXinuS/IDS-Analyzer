import dash
from dash import html

dash.register_page(__name__, path="/dos/goldeneye")

layout = html.Div([
    html.H3("GoldenEye"),
    html.P("AHello world"),
])
