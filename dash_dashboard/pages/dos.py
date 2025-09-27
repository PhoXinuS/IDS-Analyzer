import dash
from dash import html

dash.register_page(__name__, path="/dos")

layout = html.Div([
    html.H3("Dos - General Information"),
    html.P("Summary of DoS attacks."),
])
