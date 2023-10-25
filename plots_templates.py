import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from joined_data_health import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# testing data
df = health_df
pmdf = who_pm25df

# data_2019 = df[df['Year'] == 2019]
column1 = "Deaths that are from all causes attributed to household air pollution from solid fuels per 100,000 people, in both sexes aged age-standardized"
column2 = "Deaths that are from all causes attributed to ambient particulate matter pollution per 100,000 people, in both sexes aged age-standardized"
column3 = "Deaths that are from all causes attributed to air pollution per 100,000 people, in both sexes aged age-standardized"
column4 = "Deaths that are from all causes attributed to ambient ozone pollution per 100,000 people, in both sexes aged age-standardized"
columns_to_display = df.columns[3:].tolist()


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
    ], style={
        'padding': '10px 5px'
    }),

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
    pmdff = pmdf[pmdf['Year'] == year_value]


    # fig = px.scatter(
    #     dff,
    #     x=xaxis_column_name,
    #     y=yaxis_column_name,
    #     hover_name=dff['Location']
    # )

    fig = px.scatter(
        pmdff,
        x='Year',
        y='FactValueNumeric',
        hover_name=dff['Location']
    )

    # fig.update_traces(customdata=dff['Location'])

    # fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    # fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_traces(customdata=pmdff['Location'])

    fig.update_xaxes(title='Year', type='linear')# if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title='FactValueNumeric', type='linear')# if yaxis_type == 'Linear' else 'log')
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
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value'))
def update_y_timeseries(hoverData, yaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata'] 
    dff = df[df['Location'] == country_name]
    # Ensure that the selected yaxis_column_name is a valid column name
    if yaxis_column_name in dff.columns:
        title = f"<b>{country_name}</b><br>{yaxis_column_name}"
        return create_time_series(dff, yaxis_column_name, axis_type, title)
    else:
        # Handle the case where the selected column does not exist
        return go.Figure()


if __name__ == '__main__':
    app.run(debug=True)