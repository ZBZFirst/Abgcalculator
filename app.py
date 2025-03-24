import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

def calculate_pH(PaCO2, HCO3):
    pK = 6.1
    PCO2_conversion = 0.03
    pH = pK + np.log10(HCO3 / (PCO2_conversion * PaCO2))
    return pH

def classify_abg(pH, PaCO2, HCO3):
    if pH < 7.35:
        return "Acidosis"
    elif pH > 7.45:
        return "Alkalosis"
    else:
        return "Normal"

app.layout = html.Div([
    html.H1("ABG Calculator", style={'textAlign': 'center'}),

    html.Label("PaCO2"),
    dcc.Slider(id='PaCO2-slider', min=10, max=100, step=1, value=40),

    html.Label("HCO3"),
    dcc.Slider(id='HCO3-slider', min=5, max=50, step=1, value=24),

    html.Div(id='output-ph'),
    html.Div(id='output-classification'),
    dcc.Graph(id='abg-graph'),
])

@app.callback(
    [dash.dependencies.Output('output-ph', 'children'),
     dash.dependencies.Output('output-classification', 'children'),
     dash.dependencies.Output('abg-graph', 'figure')],
    [dash.dependencies.Input('PaCO2-slider', 'value'),
     dash.dependencies.Input('HCO3-slider', 'value')]
)
def update_graph(PaCO2, HCO3):
    pH = calculate_pH(PaCO2, HCO3)
    classification = classify_abg(pH, PaCO2, HCO3)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[pH], y=[HCO3], mode='markers', marker=dict(size=12, color='red')))
    fig.update_layout(title="ABG Graph", xaxis_title="pH", yaxis_title="HCO3")

    return f"pH = {pH:.2f}", f"Classification: {classification}", fig

server = app.server

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=10000, debug=True)
