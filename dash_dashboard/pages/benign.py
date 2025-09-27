import dash
from dash import html, dcc
import plotly.express as px

dash.register_page(__name__, path="/benign")

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(
    df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
    hover_name="country", log_x=True, size_max=60
)

layout = html.Div([
    html.H3("Benign"),
    dcc.Graph(figure=fig)
])
