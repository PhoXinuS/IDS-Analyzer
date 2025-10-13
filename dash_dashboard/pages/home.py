import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")


#bar chart
label_counts_df = pd.read_csv("assets/label_counts.csv")

bar_fig = go.Figure()
for _, row in label_counts_df.iterrows():
    bar_fig.add_trace(go.Bar(
        x=[row['Label']],
        y=[row['count']],
        name=row['Label']
    ))

bar_fig.update_layout(
    title_text="Distribution of Traffic Types (Full Dataset)",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Number of Occurrences",
    height=500,
    showlegend=False
)

# box chart
box_df = pd.read_csv("assets/box_flow_duration.csv", index_col='Label')

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
    title_text="Distribution of Attack Durations (Full Dataset)",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Flow Duration (Log Scale)",
    yaxis_type="log",
    height=500,
    showlegend=False
)

# violin chart
violin_df = pd.read_csv("assets/violin_avg_packet_size.csv")

violin_fig = go.Figure()
for label in sorted(violin_df['Label'].unique()):
    data = violin_df[violin_df['Label'] == label]['Average Packet Size']
    violin_fig.add_trace(go.Violin(
        y=data,
        name=label,
        box_visible=True,
        meanline_visible=True
    ))

violin_fig.update_layout(
    title_text="Distribution of Average Packet Sizes (Full Dataset)",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Average Packet Size",
    height=500,
    showlegend=False
)

# stacked bar chart
protocol_df = pd.read_csv("assets/stacked_box_protocol_distribution.csv")

stacked_fig = go.Figure()
for protocol_name in ['TCP', 'UDP', 'Other']:
    plot_data = protocol_df[protocol_df['Protocol_Name'] == protocol_name]
    if not plot_data.empty:
        stacked_fig.add_trace(go.Bar(
            x=plot_data['Label'],
            y=plot_data['Percentage'],
            name=protocol_name
        ))

stacked_fig.update_layout(
    barmode='stack',
    title_text="Percentage Distribution of Protocols by Attack Type",
    xaxis_title="Attack Type (Label)",
    yaxis_title="Percentage (%)",
    height=500,
    legend_title_text='Protocol',
    xaxis={'categoryorder': 'total descending'}
)

# scatter log chart
scatter_df = pd.read_csv("assets/scatter_packet_len.csv")

scatter_df = scatter_df[
    (scatter_df['Total Length of Fwd Packets'] > 0) &
    (scatter_df['Total Length of Bwd Packets'] > 0)
]

scatter_fig = go.Figure()
for label in sorted(scatter_df['Label'].unique()):
    data = scatter_df[scatter_df['Label'] == label]
    scatter_fig.add_trace(go.Scatter(
        x=data['Total Length of Fwd Packets'],
        y=data['Total Length of Bwd Packets'],
        name=label,
        mode='markers',
        marker=dict(size=5, opacity=0.7),
        text=data['Label'],
        hovertemplate="Label: %{text}<br>Fwd: %{x}<br>Bck: %{y}<extra></extra>"
    ))

scatter_fig.update_layout(
    title_text="Relationship between Forward and Backward Packets (Log Scale)",
    xaxis_title="Total Fwd Packets (Log Scale)",
    yaxis_title="Total Backward Packets (Log Scale)",
    height=500,
    legend_title_text='Attack Type',
    xaxis_type="log",
    yaxis_type="log"
)



# --------
layout = html.Div([
    html.H3("Benign Traffic and Attack Overview", className="mb-4"),

# switching charts (first one)
dbc.Card([
    dbc.CardBody([

        html.Div([
            html.Span("Type:", style={"font-weight": "500", "margin-right": "0.5rem"}),

            dcc.RadioItems(
                id='chart-switch',
                options=[
                    {'label': 'Sunburst (Pie)', 'value': 'pie'},
                    {'label': 'Bar Chart', 'value': 'bar'}
                ],
                value='pie',
                inline=True,
                inputStyle={"margin-right": "6px"}, 
                labelStyle={"margin-right": "15px"},
                style={"display": "inline-block", "verticalAlign": "middle"}
            )
        ], style={
            "display": "flex",
            "justify-content": "flex-end",  
            "align-items": "center",
            "margin-bottom": "0.5rem"
        }),

        html.Div(id='chart-display'), 

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
            dcc.Graph(figure=box_fig),
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
            dcc.Graph(figure=violin_fig),
            dbc.Alert(
                "Lorem ipsum "
                "Lorem ipsum 2",
                color="secondary",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),

    # card 4
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=stacked_fig),
            dbc.Alert(
                "Lorem ipsum "
                "Lorem ipsum 2",
                color="primary",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),


    # card 5
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(figure=scatter_fig),
            dbc.Alert(
                "Lorem ipsum "
                "Lorem ipsum 2",
                color="info",
                className="mt-2",
                style={"font-size": "0.9rem"}
            )
        ])
    ], className="mb-4 shadow-sm"),
])

@dash.callback(
    Output('chart-display', 'children'),
    Input('chart-switch', 'value')
)
def display_chart(chart_type):
    if chart_type == 'pie':
        return html.Iframe(
            src='/assets/attack_dist_sunburst.html',
            style={'width': '100%', 'height': '500px', 'border': 'none'}
        )
    else:
        return dcc.Graph(figure=bar_fig)
