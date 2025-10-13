import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/brute")


# box chart
box_df = pd.read_csv("assets/box_flow_bruteforce.csv", index_col='Label')

box_fig = go.Figure()
for label, row in box_df.iterrows():
    box_fig.add_trace(go.Box(
        x=[label],
        name=label,
        q1=[row['q1']],
        median=[row['median']],
        q3=[row['q3']],
        lowerfence=[row['min']],
        upperfence=[row['max']],
        boxpoints=False
    ))

box_fig.update_layout(
    title_text="Time Duration of Brute Force Attacks",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Flow Duration (Log Scale)",
    yaxis_type="log",
    height=700,
    showlegend=False
)


# bar chart
bar_df = pd.read_csv("assets/bar_flags_bruteforce.csv")

bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(
    x=bar_df['Label'],
    y=bar_df['SYN Flag Count'],
    name='SYN Flag Count',
    marker_color='royalblue'
))
bar_fig.add_trace(go.Bar(
    x=bar_df['Label'],
    y=bar_df['FIN Flag Count'],
    name='FIN Flag Count',
    marker_color='orange'
))

bar_fig.update_layout(
    barmode='group',
    title_text="Average SYN/FIN Flags in Brute Force Attacks",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Average Flag Count",
    height=700,
    showlegend=True
)


# box chart (Patator)
patator_df = pd.read_csv("assets/box_iat_patator.csv")

patator_fig = go.Figure()
for label in ['FTP-Patator', 'SSH-Patator', 'BENIGN']:
    data_for_label = patator_df[patator_df['Label'] == label]['Flow IAT Mean']
    patator_fig.add_trace(go.Box(
        y=data_for_label,
        name=label,
        boxpoints='outliers'
    ))

patator_fig.update_layout(
    title_text='Box Plot of Flow IAT Mean (Patator Attacks vs. BENIGN)',
    xaxis_title_text='Traffic Type',
    yaxis_title_text='Flow IAT Mean (Log Scale)',
    height=700,
    showlegend=True,
    yaxis_type='log'
)



layout = html.Div([
    html.H3("Brute Force Attack Analysis", className="mb-4"),

    # card 1
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=box_fig),
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
            dcc.Graph(figure=patator_fig),
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
