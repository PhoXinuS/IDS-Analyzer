import dash
from dash import html

dash.register_page(__name__, path="/patator/ssh")

layout = html.Div([
    html.H3("SSH"),
    html.P("Hello world."),
])
