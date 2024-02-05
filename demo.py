#pandas is a data manipulation library
import pandas as pd

#dash is a web application framework
#dcc is a library for creating dash components
#html is a library for creating html components
from dash import dcc
from dash import html

#plotly is a graphing library
from plotly.graph_objs import Figure
import dash

# Get the data from the API
url = "https://api.covidtracking.com/v1/states/current.csv"

# This reads the data from the API and stores it in a pandas DataFrame
data = pd.read_csv(url)

#data.shape returns the dimensions of the data
#print(data.shape)  # Check the dimensions of the data

#This creates html layout for the dashboard. One hashtag means h1, two hashtags means h2, and so on.
layout = html.Div([
    dcc.Markdown("# Interactive COVID-19 Cases of US States Dashboard"),
    dcc.Markdown("## Date: Early March 2021")
])

#This creates a figure for the dashboard
#data["state"].unique() returns the unique values in the state column
states = data["state"].unique()
#data.groupby("state")["positive"].sum() groups the data by state and sums the positive cases
confirmed_cases = data.groupby("state")["positive"].sum()

#This creates a figure for the dashboard
fig = Figure(
    #data is a list of dictionaries
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

#dcc.Graph(figure=fig) creates a graph for the dashboard
layout = html.Div([layout, dcc.Graph(figure=fig)])

#This creates a dashboard with __name__ as the name of the dashboard
#__name__ is a special variable in Python that returns the name of the current module
demo = dash.Dash(__name__)
demo.layout = layout

#Check if the code is being run as the main program
if __name__ == "__main__":
    demo.run_server(debug=True)