# dash_app.py
import dash
import plotly.graph_objs as go
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
        red_data = filtered_data[filtered_data['PM 2.5 Airpollution'] > 35]
        orange_data = filtered_data[(filtered_data['PM 2.5 Airpollution'] >= 12) & (filtered_data['PM 2.5 Airpollution'] <= 35)]
        green_data = filtered_data[(filtered_data['PM 2.5 Airpollution'] < 12)]

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
    
    return dash_app



def add_header(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
# - - - - - - - - - - - - - - SECOND PLOT - - - - - - - - - - - - - -  
def second_plot(server):
    df_mean = pd.read_csv("data_sets/air_quality/pm25_mean.csv")  
    df_min = pd.read_csv("data_sets/air_quality/pm25_min.csv")  
    df_max = pd.read_csv("data_sets/air_quality/pm25_max.csv")


    # Define columns to plot
    years = df_mean.columns[2:12].tolist()
    countries = df_mean.iloc[1:192, 0].tolist()
    continents = df_mean.iloc[1:192, 1].tolist()

    pm_mean = df_mean.iloc[1:192, 2:12].values.tolist()
    pm_min = df_min.iloc[1:192, 2:12].values.tolist()
    pm_max = df_max.iloc[1:192, 2:12].values.tolist()

    # Define a colour map for the continents

    continent_colour_map = {
        'Africa': 'brown','America': 'green','Asia': 'red', 'Europe': 'orange','Oceania': 'blue'}


    # Initialise Dash
    app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dash2/')

    app.layout = html.Div([
        html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=countries[167]
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
        
        
    # Add traces for WHO Air Quality Guidelines

        fig.add_trace(go.Scatter(x=('2015', '2018'), y=(10, 10), 
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
            title=f'Fine air particles smaller than 2.5 mircometers: {selected_country}',
            xaxis_title='Year',
            yaxis_title='PM2.5 (µg/m³)',
            yaxis_range=[0,115],
            legend=dict(title='Parameter')
            )

        return fig



    return app