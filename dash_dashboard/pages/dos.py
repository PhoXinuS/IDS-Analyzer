import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/dos")


# box chart
box_df = pd.read_csv("assets/box_flow_packets_dos.csv", index_col='Label')

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
    title_text="Comparison of Flow Packets/s for DoS and DDoS Attacks",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Flow Packets/s (Log Scale)",
    yaxis_type="log",
    height=500,
    showlegend=False
)


# histogram
histogram_df = pd.read_csv("assets/histogram_dos.csv")

histogram_fig = go.Figure()

histogram_fig.add_trace(go.Histogram(
    x=histogram_df[histogram_df['Label'] == 'DoS slowloris']['Flow IAT Mean'],
    name='DoS slowloris',
    marker_color='red',
    opacity=0.7,
    histnorm='probability density'
))

histogram_fig.add_trace(go.Histogram(
    x=histogram_df[histogram_df['Label'] == 'BENIGN']['Flow IAT Mean'],
    name='BENIGN',
    marker_color='blue',
    opacity=0.6,
    histnorm='probability density'
))

histogram_fig.update_layout(
    barmode='overlay',
    title_text='Distribution of Flow IAT Mean (DoS slowloris vs. BENIGN)',
    xaxis_title_text='Flow IAT Mean (Log Scale)',
    yaxis_title_text='Density',
    height=500,
    legend_title_text='Traffic Type'
)


# density chart
density_df = pd.read_csv("assets/density_dos.csv")

hulk_data = density_df[density_df['Label'] == 'DoS Hulk']['Total Length of Fwd Packets']
goldeneye_data = density_df[density_df['Label'] == 'DoS GoldenEye']['Total Length of Fwd Packets']

hist_data = [hulk_data, goldeneye_data]
group_labels = ['DoS Hulk', 'DoS GoldenEye']

density_fig = ff.create_distplot(
    hist_data,
    group_labels,
    bin_size=.2,
    show_hist=False,
    show_rug=False
)

density_fig.update_layout(
    title_text='Density of Fwd Packet Length (DoS Hulk vs. DoS GoldenEye)',
    xaxis_title_text='Total Length of Fwd Packets',
    yaxis_title_text='Density',
    height=500,
    legend_title_text='Attack Type'
)



layout = html.Div([
    html.H3("DoS and DDoS Attack Analysis", className="mb-4"),

    # card 1
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=box_fig),
            # dbc.Alert(
            #     [
            #         html.I(className="bi bi-info-circle"),
            #         "Lorem ipsum 2",
            #     ],
            #     color="primary",
            #     className="mt-2",
            #     style={"font-size": "0.9rem"}
            # )
        ])
    ], className="mb-4 shadow-sm"),

    # card 2
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=histogram_fig),
            dbc.Alert(
                " As slowloris aims to maintain as many connections as possible and, in comparison to other DoS attacks, works slowly, it can be clearly seen having longer Inter-Arrival Time between to packets.",
                color="info",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),

    # card 3
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=density_fig),
            # dbc.Alert(
            #     "Lorem ipsum "
            #     "Lorem ipsum 2",
            #     color="secondary",
            #     className="mt-2",
            #     style={"font-size": "0.9rem"}
            # )
        ])
    ], className="mb-4 shadow-sm"),
])
