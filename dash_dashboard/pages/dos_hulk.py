import dash
from dash import html

dash.register_page(__name__, path="/dos/hulk")

layout = html.Div([
    html.H3("Hulk"),
    html.P("Hello world."),
])
