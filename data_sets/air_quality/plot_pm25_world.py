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
countries = df_mean.iloc[:, 0].tolist()
continents = df_mean.iloc[:, 1].tolist()

pm_mean = df_mean.iloc[:, 2:12].values.tolist()

# Setting the colour map
continent_colour_map = {
    'Africa': 'brown','America': 'green','Asia': 'red', 'Europe': 'orange','Oceania': 'blue'}

# Creating the Dash plot/app
app = dash.Dash(__name__)

fig = go.Figure()

for country_index, country in enumerate(countries):
    selected_pm_mean = pm_mean[country_index]
    selected_continent = continents[country_index]

    fig.add_trace(go.Scatter(x=years, y=selected_pm_mean, 
                            mode='lines', line=dict(dash='solid', width=1, color=continent_colour_map[selected_continent]), 
                            name=f'{selected_continent} Mean'))

# Create buttons for custom legend
legend_items = [
    dict(label=continent, method='restyle', 
         args=['visible', [True if trace.name.startswith(continent) else False for trace in fig.data]])
    for continent in continent_colour_map.keys()
]

# Add button to show all continents together
legend_items.append(
    dict(label='Show All', method='restyle', 
         args=['visible', [True] * len(fig.data)])
)

# Set layout
fig.update_layout(
    title=f'Fine air particulates worldwide 2010-2019',
    xaxis_title='Year',
    yaxis_title='PM2.5 (µg/m³)',
    yaxis_range=[0, 115],
    showlegend=False,  # Remove the right-hand legend
    updatemenus=[
        dict(
            type='buttons',
            showactive=False,
            buttons=legend_items
        )
    ]
)

# Adjust legend position
fig.update_layout(legend=dict(x=1, y=0.5))

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=4500)
