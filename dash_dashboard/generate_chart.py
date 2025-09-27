import plotly.express as px

df = px.data.gapminder().query("year == 2007")

fig = px.scatter(
    df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
    hover_name="country", log_x=True, size_max=60
)

fig.write_html("chart.html", include_plotlyjs="cdn")
