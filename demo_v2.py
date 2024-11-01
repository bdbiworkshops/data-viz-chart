#Working with Dash and Plotly to create an interactive COVID-19 dashboard for US states for late 2020 and early 2021.
#Using a public dataset for the purposes of a workshop. Using an API with an API key is recommended for production.
#The response from the API request should be parsed or utilized differently based on the structure of the data, since it may not be a CSV file.

# Importing necessary libraries for data handling, interactive dashboard, and data visualization
import pandas as pd  # Pandas for data manipulation and analysis
from dash import dcc, html, Input, Output  # Dash components for dashboard layout and interactivity
import dash  # Dash for creating web applications with Python
from plotly.graph_objs import Figure, Bar  # Plotly for creating charts and figures
import plotly.express as px  # Plotly Express for easy-to-use chart functions

# Load the COVID-19 data from an external API as a CSV into a Pandas DataFrame
url = "https://api.covidtracking.com/v1/states/current.csv"
data = pd.read_csv(url)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([  # Use a Div component to structure the layout
    # Dashboard title and subtitle using Markdown components
    dcc.Markdown("# COVID-19 Dashboard for US States"),
    dcc.Markdown("## Tracking Metrics and Trends Across States for Late 2020 and Early 2021"),

    # Create tab structure for organizing multiple data visualizations
    dcc.Tabs([
        # First tab: "Overview"
        dcc.Tab(label="Overview", children=[
            html.Div([
                dcc.Graph(id="cases-bar-chart"),  # Bar chart for total confirmed cases per state
                dcc.Graph(id="testing-deaths-scatter")  # Scatter plot for total tests vs deaths
            ]),
        ]),
        # Second tab: "Detailed Metrics" with a dropdown for selecting individual states
        dcc.Tab(label="Detailed Metrics", children=[
            html.Div([
                dcc.Markdown("### Select State for Detailed Analysis"),  # Header for state selection
                # Dropdown menu to select a specific state for detailed metrics
                dcc.Dropdown(
                    id="state-dropdown",  # Dropdown component ID for callback access
                    options=[{"label": state, "value": state} for state in data["state"].unique()],  # List of states
                    value="CA",  # Default state selection (California)
                    clearable=False,  # Disable clear button
                    placeholder="Select a state"  # Placeholder text
                ),
                dcc.Graph(id="hospitalization-chart"),  # Chart for hospitalization metrics
                dcc.Graph(id="death-rate-chart")  # Chart for death rate calculation
            ])
        ]),
    ])
])

# Define callback to update the bar chart of confirmed cases based on state selection
@app.callback(
    Output("cases-bar-chart", "figure"),
    Input("state-dropdown", "value")  # Input from state dropdown selection
)
def update_cases_bar_chart(state):
    # Calculate total confirmed cases per state
    cases_data = data.groupby("state")["positive"].sum().reset_index()
    # Create bar chart for confirmed cases
    fig = px.bar(cases_data, x="state", y="positive", title="Total Confirmed COVID-19 Cases by State")
    fig.update_layout(xaxis_title="State", yaxis_title="Confirmed Cases")
    return fig

# Define callback to update the scatter plot of tests vs. deaths by state
@app.callback(
    Output("testing-deaths-scatter", "figure"),
    Input("state-dropdown", "value")  # Input from state dropdown selection
)
def update_testing_deaths_scatter(state):
    # Create a scatter plot showing the relationship between total tests and deaths by state
    fig = px.scatter(data, x="totalTestResults", y="death", color="state",
                     hover_name="state", title="Total Tests vs Deaths by State")
    fig.update_layout(xaxis_title="Total Tests", yaxis_title="Deaths")
    return fig

# Define callback to update the bar chart of hospitalizations for the selected state
@app.callback(
    Output("hospitalization-chart", "figure"),
    Input("state-dropdown", "value")  # Input from state dropdown selection
)
def update_hospitalization_chart(state):
    # Filter data for the selected state
    selected_data = data[data["state"] == state]
    # Create bar chart showing current and cumulative hospitalizations
    fig = Figure(data=[
        Bar(name="Hospitalized Currently", x=["Hospitalized"], y=[selected_data["hospitalizedCurrently"].values[0]]),
        Bar(name="Hospitalized Cumulative", x=["Hospitalized"], y=[selected_data["hospitalizedCumulative"].values[0]])
    ])
    fig.update_layout(barmode="group", title=f"Current vs. Cumulative Hospitalizations in {state}")
    return fig

# Define callback to update the death rate bar chart for the selected state
@app.callback(
    Output("death-rate-chart", "figure"),
    Input("state-dropdown", "value")  # Input from state dropdown selection
)
def update_death_rate_chart(state):
    # Calculate death rate for the selected state
    selected_data = data[data["state"] == state]
    death_rate = (selected_data["death"].values[0] / selected_data["positive"].values[0]) * 100
    # Create bar chart showing the death rate
    fig = px.bar(x=["Death Rate"], y=[death_rate], title=f"Death Rate in {state}", labels={"x": "Metric", "y": "Rate (%)"})
    return fig

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
#Localhost:8050
#Run with the command python {file name} in the terminal
#Open the browser and go to http://{localhost}:8050/ to view the dashboard