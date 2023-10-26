# dash_app.py
import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import os

def init_dash(server):
    CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    stylesheet= CURR_DIR_PATH + '\\static\\css\\styles.css'
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dash/',
        external_stylesheets=[stylesheet]
    )
    # final data
    # CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(CURR_DIR_PATH+'.\\health_and_air_final_df.csv')

    columns_to_display = df.columns[3:-2].tolist()

    dash_app.layout = html.Div([
        html.H1("Health and Air Quality"),
        # Dropdown menu for selecting a country
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Location'].unique()],
            value='Sweden',  # Default selected country
            style={
            'width': '90%',  # Set the width to 80%
            'margin': 'auto',  # Center the dropdown horizontally
            'color': 'blue',  # Set the text color to blue
            #'background-color': 'lightgray',  # Set the background color to light gray
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
            #'background-color': 'lightgray',  # Set the background color to light gray
            '@media screen and (max-width: 600px)': {
            'width': '90%',
        }}),
        
        # Plot to show values of the selected column over the years
        dcc.Graph(id='line-plot'),
        
        # Plot to show PM2.5 pollution for the selected country
        dcc.Graph(id='pm25-plot')
    ], style = {
        'width': '80%',
        'margin': 'auto',
        'display': 'inline-block',
        '@media screen and (max-width: 600px)': {
            'width': '90%',
        }
    })

    # callback to update the line plot
    @app.callback(
        Output('line-plot', 'figure'),
        Input('country-dropdown', 'value'),
        Input('column-dropdown', 'value')
    )
    def update_line_plot(selected_country, selected_column):
        filtered_data = df[(df['Location'] == selected_country)]
        figure = px.line(filtered_data, x='Year', y=selected_column, title=f"{selected_country} - {selected_column}")
        figure.update_yaxes(title_text='per 100.000 people') # Standard value for all graphs
        return figure

    # callback to update the PM2.5 pollution plot based on country
    @app.callback(
        Output('pm25-plot', 'figure'),
        Input('country-dropdown', 'value')
    )
    def update_pm25_plot(selected_country):
        filtered_data = df[(df['Location'] == selected_country)]
        figure = px.line(filtered_data, x='Year', y='PM 2.5 Airpollution', title=f"{selected_country} - PM2.5 Air Pollution")
        figure.update_yaxes(title_text='PM 2.5') # Standard value for all graphs
        return figure
    
    return dash_app



def add_header(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response