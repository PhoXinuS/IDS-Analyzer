import dash
from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
    ]
)
server = app.server

NAVBAR_STYLE = {
    "display": "flex",
    "justify-content": "space-between",
    "align-items": "center",
    "padding": "0.75rem 2rem",
    "background-color": "#f8f9fa",
    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
    "position": "sticky",
    "top": 0,
    "zIndex": 1000
}

CONTENT_STYLE = {"padding": "2rem 2rem"}

dropdown_options = [
    {"label": " Data Distribution", "value": "/"},
    {"label": " DoS Attacks", "value": "/dos"},
    {"label": " Brute Force Attacks", "value": "/brute"},
    {"label": " Web Attacks", "value": "/web"},
]

navbar = html.Div([
    html.H4("IDS Analyzer Dashboard", className="m-0", style={"color": "#0A9EBC"}),

    dcc.Dropdown(
        id="page-selector",
        options=dropdown_options,
        value="/",
        clearable=False,
        style={
            "width": "280px",
            "borderRadius": "8px",
            "font-size": "0.95rem"
        },
    )
], style=NAVBAR_STYLE)

content = html.Div(dash.page_container, style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content
])

@app.callback(
    Output("url", "pathname"),
    Output("page-selector", "value"),
    Input("page-selector", "value"),
    Input("url", "pathname"),
    prevent_initial_call=False
)

def sync_url_and_dropdown(drop_value, url_path):
    triggered = ctx.triggered_id

    if triggered == "page-selector":
        return drop_value, drop_value
    elif triggered == "url": 
        return url_path, url_path
    else: 
        return "/", "/"

if __name__ == "__main__":
    app.run(debug=True)
