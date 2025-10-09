import dash
from dash import html

dash.register_page(__name__, path="/patator")

layout = html.Div([
    html.H3("Patator - General Information"),
    html.P("Summary of Patator attacks."),
])
