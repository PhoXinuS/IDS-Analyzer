import dash
from dash import html

dash.register_page(__name__, path="/dos/slowloris")

layout = html.Div([
    html.H3("Slowloris"),
    html.P("Hello world."),
])
