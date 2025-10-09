import dash
from dash import html

dash.register_page(__name__, path="/bot")

layout = html.Div([
    html.H3("Bot"),
    html.P("Hello world"),
])
