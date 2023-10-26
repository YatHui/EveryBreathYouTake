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


app.layout = html.Div([
    html.Div([
        html.Div([
        dcc.Dropdown(
            options=[{'label': column, 'value': column} for column in columns_to_display],
            value=columns_to_display[0],  # Default selected column
            id='crossfilter-xaxis-column',
        ),
        dcc.RadioItems(
            options=[{'label': 'Linear', 'value': 'linear'}, {'label': 'Log', 'value': 'log'}],
            value='linear',  # Default selection
            id='crossfilter-xaxis-type',
            labelStyle={'display': 'inline-block', 'marginTop': '5px'}
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            options=[{'label': column, 'value': column} for column in columns_to_display],
            value=columns_to_display[1],  # Default selected column
            id='crossfilter-yaxis-column',
        ),
        dcc.RadioItems(
            ['Linear', 'Log'],
            'Linear',
            id='crossfilter-yaxis-type',
            labelStyle={'display': 'inline-block', 'marginTop': '5px'}
        )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '10px 5px'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Sweden'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        id='crossfilter-year--slider',
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    fig = px.scatter(
        dff,
        x=xaxis_column_name,
        y=yaxis_column_name,
        hover_name=dff['Location'],
    )

    fig.update_traces(customdata=dff['Location'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, yaxis_column_name, axis_type, title):

    fig = px.scatter(dff, x='Year', y=yaxis_column_name)

    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Location'] == country_name]

    if xaxis_column_name in dff.columns:
        title = f"<b>{country_name}</b><br>{xaxis_column_name}"
        return create_time_series(dff, xaxis_column_name, axis_type, title)
    else:
        # Handle the case where the selected column does not exist
        return go.Figure()

@callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-type', 'value'))
def update_y_timeseries(hoverData, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Location'] == country_name]

    # Ensure that 'pollution' is always used as the y-axis column
    yaxis_column_name = 'PM 2.5 Airpollution'

    title = f"<b>{country_name}</b><br>{yaxis_column_name}"
    return create_time_series(dff, yaxis_column_name, axis_type, title)



if __name__ == '__main__':
    app.run(debug=True)