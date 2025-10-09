import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H3("General Overview of all attacks"),
    html.Iframe(
        src="/assets/attack_sunburst_interactive.html",
        style={"width": "100%", "height": "600px", "border": "none"}
    )
])
