import dash
from dash import html

dash.register_page(__name__, path="/dos/ddos")

layout = html.Div([
    html.H3("DDOS"),
    html.P("Hello world"),
])
