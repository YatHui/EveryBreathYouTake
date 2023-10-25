# dash_app.py

import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import html
from dash import dcc

def init_dash(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dash/'
    )

    dash_app.layout = html.Div([
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])

    return dash_app


def add_header(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
