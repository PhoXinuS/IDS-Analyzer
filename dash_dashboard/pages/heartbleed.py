import dash
from dash import html

dash.register_page(__name__, path="/heartbleed")

layout = html.Div([
    html.H3("Heartbleed - General Information"),
    html.P("Summary of Heartbleed attacks."),
])
