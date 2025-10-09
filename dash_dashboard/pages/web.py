import dash
from dash import html

dash.register_page(__name__, path="/web")

layout = html.Div([
    html.H3("Web Attacks - General Information"),
    html.P("Summary of Web attacks."),
])
