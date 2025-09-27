import dash
from dash import html

dash.register_page(__name__, path="/web/sqlinjection")

layout = html.Div([
    html.H3("SQL Injection"),
    html.P("Hello world."),
])
