import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/benign")

csv_path = "assets/label_counts.csv"
label_counts_df = pd.read_csv(csv_path)


fig = go.Figure()

for _, row in label_counts_df.iterrows():
    fig.add_trace(go.Bar(
        x=[row['Label']],
        y=[row['count']],
        name=row['Label']
    ))

fig.update_layout(
    title_text="Distribution of Traffic Types (Full Dataset)",
    xaxis_title="Traffic/Attack Type (Label)",
    yaxis_title="Number of Occurrences",
    height=600,
    showlegend=False
)


layout = html.Div([
    html.H3("Benign Traffic Analysis"),

    dcc.Graph(figure=fig),


    dbc.Alert(
        [
            html.I(className="bi bi-info-circle-fill me-2"),
            html.Span(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Sed ut perspiciatis unde omnis iste natus error sit voluptatem "
                "accusantium doloremque laudantium, totam rem aperiam, eaque ipsa "
                "quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."
            )
        ],
        color="primary",
        className="mt-3",
        style={
            "font-size": "0.9rem",
            "background-color": "#eef5ff",
            "border": "1px solid #cce0ff",
            "color": "#0d47a1"
        }
    )
])
