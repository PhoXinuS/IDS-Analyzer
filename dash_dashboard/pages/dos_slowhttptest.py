import dash
from dash import html

dash.register_page(__name__, path="/dos/slowhttptest")

layout = html.Div([
    html.H3("SlowHTTPTest"),
    html.P("Hello world."),
])
