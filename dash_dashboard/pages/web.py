import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/web")


# violin chart
violin_df = pd.read_csv("assets/violin_webattack_samples.csv")

violin_fig = go.Figure()
for label in sorted(violin_df['Label'].unique()):
    data = violin_df[violin_df['Label'] == label]['Fwd Packet Length Max']
    violin_fig.add_trace(go.Violin(
        y=data,
        name=label,
        box_visible=True,
        meanline_visible=True
    ))

violin_fig.update_layout(
    title_text="Distribution of Fwd Packet Length Max for Selected Web Attacks and BENIGN (Ports 80/443)",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Fwd Packet Length Max",
    height=500,
    showlegend=False
)


# bar chart
bar_df = pd.read_csv("assets/bar_down_up_infiltration.csv")

bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(
    x=bar_df['Label'],
    y=bar_df['Down/Up Ratio'],
    marker_color=['crimson', 'green']
))

bar_fig.update_layout(
    title_text='Average Down/Up Ratio (Infiltration vs. BENIGN)',
    xaxis_title='Traffic Type',
    yaxis_title='Average Down/Up Ratio',
    height=500,
    showlegend=False
)


# box chart
box_df = pd.read_csv("assets/box_web_idle.csv")

ordered_labels = [
    'Infiltration',
    'PortScan',
    'Web Attack  Sql Injection',
    'BENIGN'
]

box_fig = go.Figure()
for label in ordered_labels:
    data_for_label = box_df[box_df['Label'] == label]['Idle Mean']
    box_fig.add_trace(go.Box(
        y=data_for_label,
        name=label,
        boxpoints='outliers'
    ))

box_fig.update_layout(
    title_text='Idle Time Distribution by Traffic Type',
    xaxis_title_text='Traffic Type',
    yaxis_title_text='Idle Mean (Log Scale)',
    height=500,
    showlegend=True,
    yaxis_type='log'
)



layout = html.Div([
    html.H3("Web Attack Analysis", className="mb-4"),

    # card 1
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=violin_fig),
            dbc.Alert(
                "Lorem ipsum "
                "Lorem ipsum 2",
                color="primary",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),

    # card 2
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=bar_fig),
            dbc.Alert(
                "Lorem ipsum "
                "Lorem ipsum 2",
                color="info",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),

    # card 3
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=box_fig),
            dbc.Alert(
                "Lorem ipsum "
                "Lorem ipsum 2",
                color="secondary",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),
])
