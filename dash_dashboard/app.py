import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"]
)
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow-y": "auto", 
    "overflow-x": "hidden",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H2("Menu", className="display-6"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("General Information", href="/", active="exact"),

                dbc.NavLink("Pho and Sakura", href="/pholovessakura", active="exact"),

                dbc.NavLink("Benign", href="/benign", active="exact"),

                # DoS Attacks
                html.Div(
                    [
                        dbc.NavLink(
                            "DoS Attacks",
                            href="/dos",
                            active="exact",
                            id="dos-link",
                            style={"width": "calc(100% - 30px)", "display": "inline-block"}
                        ),
                        html.I(
                            className="bi bi-chevron-down",
                            id="dos-toggle",
                            style={
                                "float": "right",
                                "padding-right": "10px",
                                "cursor": "pointer",
                                "font-size": "1.2rem",
                                "color": "#0d6efd"
                            }
                        )
                    ],
                    style={"width": "100%", "display": "flex", "align-items": "center"}
                ),

                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavLink("DDoS Attack", href="/dos/ddos", active="exact", style={"padding-left": "2rem"}),
                            dbc.NavLink("Slowloris Attack", href="/dos/slowloris", active="exact", style={"padding-left": "2rem"}),
                            dbc.NavLink("Hulk Attack", href="/dos/hulk", active="exact", style={"padding-left": "2rem"}),
                            dbc.NavLink("GoldenEye Attack", href="/dos/goldeneye", active="exact", style={"padding-left": "2rem"}),
                            dbc.NavLink("SlowHTTPTest Attack", href="/dos/slowhttptest", active="exact", style={"padding-left": "2rem"}),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                    id="collapse-dos",
                    is_open=False,
                ),

                # Web Attacks
                html.Div(
                    [
                        dbc.NavLink(
                            "Web Attacks",
                            href="/web",
                            active="exact",
                            id="web-link",
                            style={"width": "calc(100% - 30px)", "display": "inline-block"}
                        ),
                        html.I(
                            className="bi bi-chevron-down",
                            id="web-toggle",
                            style={
                                "float": "right",
                                "padding-right": "10px",
                                "cursor": "pointer",
                                "font-size": "1.2rem",
                                "color": "#0d6efd"
                            }
                        )
                    ],
                    style={"width": "100%", "display": "flex", "align-items": "center"}
                ),

                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavLink("Bruteforce Attack", href="/web/bruteforce", active="exact", style={"padding-left": "2rem"}),
                            dbc.NavLink("XSS Attack", href="/web/xss", active="exact", style={"padding-left": "2rem"}),
                            dbc.NavLink("SQL Injection Attack", href="/web/sqlinjection", active="exact", style={"padding-left": "2rem"}),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                    id="collapse-web",
                    is_open=False,
                ),

                # Patator Attacks
                html.Div(
                    [
                        dbc.NavLink(
                            "Patator Attacks",
                            href="/patator",
                            active="exact",
                            id="patator-link",
                            style={"width": "calc(100% - 30px)", "display": "inline-block"}
                        ),
                        html.I(
                            className="bi bi-chevron-down",
                            id="patator-toggle",
                            style={
                                "float": "right",
                                "padding-right": "10px",
                                "cursor": "pointer",
                                "font-size": "1.2rem",
                                "color": "#0d6efd"
                            }
                        )
                    ],
                    style={"width": "100%", "display": "flex", "align-items": "center"}
                ),

                dbc.Collapse( 
                    dbc.Nav(
                    [
                        dbc.NavLink("SSH Patator", href="/patator/ssh", active="exact"),
                        dbc.NavLink("FTP Patator", href="/patator/ftp", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
                id="collapse-patator",
                is_open=False,
                ),

                # Other
                dbc.NavLink("Bot", href="/bot", active="exact"),
                dbc.NavLink("Heartbleed Attack", href="/heartbleed", active="exact"),
                dbc.NavLink("Infiltration", href="/infiltration", active="exact"),
                dbc.NavLink("PortScan", href="/portscan", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(dash.page_container, style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    [Output("collapse-dos", "is_open"),
     Output("dos-toggle", "className")],
    [Input("dos-toggle", "n_clicks")],
    [State("collapse-dos", "is_open")],
)
def toggle_dos(n_clicks, is_open):
    if n_clicks:
        return not is_open, "bi bi-chevron-up" if not is_open else "bi bi-chevron-down"
    return is_open, "bi bi-chevron-down"

@app.callback(
    [Output("collapse-patator", "is_open"),
     Output("patator-toggle", "className")],
    [Input("patator-toggle", "n_clicks")],
    [State("collapse-patator", "is_open")],
)
def toggle_patator(n_clicks, is_open):
    if n_clicks:
        return not is_open, "bi bi-chevron-up" if not is_open else "bi bi-chevron-down"
    return is_open, "bi bi-chevron-down"


@app.callback(
    [Output("collapse-web", "is_open"),
     Output("web-toggle", "className")],
    [Input("web-toggle", "n_clicks")],
    [State("collapse-web", "is_open")],
)
def toggle_web(n_clicks, is_open):
    if n_clicks:
        return not is_open, "bi bi-chevron-up" if not is_open else "bi bi-chevron-down"
    return is_open, "bi bi-chevron-down"


if __name__ == "__main__":
    app.run(debug=True)
