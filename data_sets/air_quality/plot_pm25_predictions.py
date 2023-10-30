import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd


# Import data

# Existing data from WHO
df_mean = pd.read_csv("data_sets/air_quality/pm25_mean.csv")  
df_min = pd.read_csv("data_sets/air_quality/pm25_min.csv")  
df_max = pd.read_csv("data_sets/air_quality/pm25_max.csv")  

# Predictions for 2020-2023
df_predict = pd.read_csv("data_sets/air_quality/predictions_pm25.csv")  


# Define columns to plot
years = df_predict.columns[2:].tolist()
countries = df_mean.iloc[:, 0].tolist()
continents = df_mean.iloc[:, 1].tolist()

pm_mean = df_mean.iloc[0:, 2:12].values.tolist()
pm_min = df_min.iloc[0:, 2:12].values.tolist()
pm_max = df_max.iloc[0:, 2:12].values.tolist()

pm_predict = df_predict.iloc[:, 11: ].values.tolist()

# Define a colour map for the continents

continent_colour_map = {
    'Africa': 'brown','America': 'green','Asia': 'red', 'Europe': 'orange','Oceania': 'blue'}


# Initialise Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value=countries[168]
        )
    ]),
    html.Div([
        dcc.Graph(id='pm-line-chart')
    ])
])

@app.callback(
    Output('pm-line-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)

# Define mean, min and max PM2.5 values to plot

def update_line_chart(selected_country):

    country_index = countries.index(selected_country)
    selected_pm_mean = pm_mean[country_index]
    selected_pm_min = pm_min[country_index]
    selected_pm_max = pm_max[country_index]

    selected_pm_predict = pm_predict[country_index]

    selected_continent = continents[country_index]

    fig = go.Figure()
    

# Add traces for Mean, Min, Max

    fig.add_trace(go.Scatter(x=years, y=selected_pm_max, 
                             mode='lines', line=dict(dash='solid', width=2), 
                             name='Max'))
    fig.add_trace(go.Scatter(x=years, y=selected_pm_mean, 
                             mode='lines', line=dict(dash='solid', width=1), 
                             name='Mean'))
    fig.add_trace(go.Scatter(x=years, y=selected_pm_min, 
                             mode='lines', line=dict(dash='solid', width=0.5), 
                             name='Min'))

# Add traces for predictions 2020-2023
    fig.add_trace(go.Scatter(x=df_predict.columns[11:16], y=selected_pm_predict, 
                             mode='lines', line=dict(dash='dot', width=1), 
                             name='Predictions'))
    
    
# Add traces for WHO Air Quality Guidelines

    fig.add_trace(go.Scatter(x=('2010', '2018'), y=(10, 10), 
                         mode='lines', 
                         line=dict(color='black', dash='dashdot', width=1), 
                         name='2005 Guidelines'))
    fig.add_trace(go.Scatter(x=('2018', '2021'), y=(5.5, 5.5), 
                         mode='lines', 
                         line=dict(color='green', dash='dashdot', width=1), 
                         name='2018 Guidelines'))
    fig.add_trace(go.Scatter(x=('2021', '2023'), y=(5, 5), 
                         mode='lines', 
                         line=dict(color='blue', dash='dashdot', width=1), 
                         name='2021 Guidelines'))

    
# Set the continent colour
    fig.update_traces(line=dict(color=continent_colour_map[selected_continent]))

    # Set layout

    fig.update_layout(
        title=f'Fine air particulates - Predictions and Goals: {selected_country}',
        xaxis_title='Year',
        yaxis_title='PM2.5 (µg/m³)',
        yaxis_range=[0,115],
        legend=dict(title='Parameter')
        )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=4003)
