import dash
from dash import html

dash.register_page(__name__, path="/web/xss")

layout = html.Div([
    html.H3("XSS"),
    html.P("Hello world."),
])
