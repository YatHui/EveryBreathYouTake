import dash
from dash import dcc, html, callback, Output, Input
import plotly.graph_objs as go
import pandas as pd

# Import data
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

continent_colour_map = {
    'Africa': 'brown','America': 'green','Asia': 'red', 'Europe': 'orange','Oceania': 'blue'}

app = dash.Dash(__name__)


fig = go.Figure()

legend_items = []

for country_index, country in enumerate(countries):
    selected_pm_mean = pm_mean[country_index]
    selected_pm_min = pm_min[country_index]
    selected_pm_max = pm_max[country_index]
    selected_continent = continents[country_index]

    # Add traces for Mean, Min, Max
    
    # fig.add_trace(go.Scatter(x=years, y=selected_pm_max, 
    #                         mode='lines', line=dict(dash='solid', width=2), 
    #                         name=f'{country} Max')),
    fig.add_trace(go.Scatter(x=years, y=selected_pm_mean, 
                            mode='lines', line=dict(dash='solid', width=1, color=continent_colour_map[selected_continent]), 
                            name=f'{selected_continent} Mean'))
    # fig.add_trace(go.Scatter(x=years, y=selected_pm_min, 
    #                         mode='lines', line=dict(dash='solid', width=0.5), 
    #                         name=f'{country} Min', 
    #                         line=dict(color=continent_colour_map[selected_continent])))

   # Store legend item for this continent
    legend_items.append(dict(
    label=selected_continent,
    method='restyle',
    args=['visible', [
        True if trace.name.startswith(selected_continent) 
        else False for trace in fig.data]]))

 # Set the continent colour
    #fig.update_traces(line=dict(color=continent_colour_map[selected_continent]))

# Set layout
fig.update_layout(
    title=f'Fine air particles smaller than 2.5 micrometers (mean values world-wide)',
    xaxis_title='Year',
    yaxis_title='PM2.5 (µg/m³)',
    yaxis_range=[0, 115],
    updatemenus=[
        dict(
            type='buttons',
            showactive=False,
            buttons=legend_items
        )
    ]
)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=4500)
