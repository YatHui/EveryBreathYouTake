import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import os

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
stylesheet= CURR_DIR_PATH + '\\static\\css\\styles.css'
app = Dash(__name__, external_stylesheets=[stylesheet])

# final data
df = pd.read_csv(CURR_DIR_PATH+'.\\health_and_air_final_df.csv')
columns_to_display = df.columns[3:-2].tolist()


# Define the layout of the app
app.layout = html.Div([
    # Dropdown menu for selecting a country
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Location'].unique()],
        value='Sweden',  # Default selected country
        style={
        'width': '90%',  # Set the width to 80%
        'margin': 'auto',  # Center the dropdown horizontally
        'color': 'blue',  # Set the text color to blue
        '@media screen and (max-width: 600px)': {
        'width': '90%',
    }}), 
    
    # Dropdown menu for selecting a column
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': column, 'value': column} for column in columns_to_display],
        value='Death from ambient particulate matter pollution',  # Default selected value
        style={
        'width': '90%',  # Set the width to 80%
        'margin': 'auto',  # Center the dropdown horizontally
        'color': 'blue',  # Set the text color to blue
        '@media screen and (max-width: 600px)': {
        'width': '90%',
    }}),
    
    # Plot to show values of the selected column over the years
    dcc.Graph(id='line-plot', 
              style = {
                'width': '100%',
                'margin': 'auto',
                'display': 'inline-block',
                '@media screen and (max-width: 600px)': {
                    'width': '100%',
                    'margin':1}}),
    
    # Plot to show PM2.5 pollution for the selected country
    dcc.Graph(id='pm25-plot', 
              style = {
                'width': '100%',
                'margin': 'auto',
                'display': 'inline-block',
                '@media screen and (max-width: 600px)': {
                    'width': '100%',
                    'margin':1}})
])

# callback to update the line plot
@callback(
    Output('line-plot', 'figure'),
    Input('country-dropdown', 'value'),
    Input('column-dropdown', 'value')
)
def update_line_plot(selected_country, selected_column):
    filtered_data = df[(df['Location'] == selected_country)]
    # Define custom colors for  line
    custom_color = ['red']
    figure = px.line(filtered_data, x='Year', 
                     y=selected_column, 
                     title=f"{selected_country}<br>{selected_column}",
                     color_discrete_sequence=custom_color)
    figure.update_yaxes(title_text='per 100.000 people') # Standard value for all graphs
    figure.update_layout(margin={'l': 40, 'b': 20, 't': 45, 'r': 2})
    return figure

# callback to update the PM2.5 pollution plot based on country
@callback(
    Output('pm25-plot', 'figure'),
    Input('country-dropdown', 'value')
)
def update_pm25_plot(selected_country):
    filtered_data = df[df['Location'] == selected_country]

    # Create a new DataFrame for each line color based on PM values
    red_data = filtered_data[filtered_data['PM 2.5 Airpollution'] > 50]
    orange_data = filtered_data[(filtered_data['PM 2.5 Airpollution'] >= 20) & (filtered_data['PM 2.5 Airpollution'] <= 50)]
    green_data = filtered_data[(filtered_data['PM 2.5 Airpollution'] < 20)]

    figure = go.Figure()

    if not red_data.empty:
        figure.add_trace(go.Scatter(x=red_data['Year'], y=red_data['PM 2.5 Airpollution'], name='Red', line=dict(color='red')))
    if not orange_data.empty:
        figure.add_trace(go.Scatter(x=orange_data['Year'], y=orange_data['PM 2.5 Airpollution'], name='Orange', line=dict(color='orange')))
    if not green_data.empty:
        figure.add_trace(go.Scatter(x=green_data['Year'], y=green_data['PM 2.5 Airpollution'], name='Green', line=dict(color='green')))

    figure.update_layout(
        title=f"{selected_country}<br>PM2.5 Air Pollution",
        yaxis_title='PM 2.5 levels',
        margin={'l': 40, 'b': 20, 't': 45, 'r': 2})
    return figure

if __name__ == '__main__':
    app.run(debug=True)