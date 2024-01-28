import requests
import pandas as pd

from dash import dcc
from dash import html

from plotly.graph_objs import Figure
import dash

url = "/Users/riapatel/Desktop/BDBI Training/dash-plotly/all-states-history.csv"

data = pd.read_csv(url)

# print(data.head())
print(data.shape)  # Check the dimensions of the data

layout = html.Div([
    dcc.Markdown("# Interactive COVID-19 Cases of US States Dashboard"),
])

states = data["state"].unique()
confirmed_cases = data.groupby("state")["positive"].sum()

fig = Figure(
    data = [
        dict(
            name = state,
            x = [state],
            y = [confirmed_cases[state]],
        )
        for state in states
    ],
    layout=dict(
        title="Confirmed COVID-19 Cases Per State",
        xaxis_title="State",
        yaxis_title="Confirmed Cases",
    ),
)

layout = html.Div([layout, dcc.Graph(figure=fig)])

demo = dash.Dash(__name__)
demo.layout = layout

if __name__ == "__main__":
    demo.run_server(debug=True)