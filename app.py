# -*- coding: utf-8 -*-

import sqlite3
import numpy as np
import pandas as pd

import dash
from dash.dependencies import Event, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Prepare data

conn = sqlite3.connect('data/transactions.db')
df = pd.read_sql("""
    SELECT date, amount
    FROM transactions
    WHERE transaction_type == 'credit' AND category <> 'Transfer'
    """, conn)
conn.close()

app = dash.Dash()

# Edit this object!
layout = html.Div([
    html.H1('Hello Dash!'),
    html.H3('Dash with live-reload'),


    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.H3('My Graph'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scatter(
                    x = df['date'],
                    y = df['amount']
                )
            ],
        ),
        id='my-graph'
    ),

    html.H3('Example Graph'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            ],
            'layout': {
                'title': 'example graph'
            }
        }
    )


])

# does not refresh
app.layout = html.Div(children=[
    dcc.Interval(id='refresh', interval=1000),
    html.Div(id='content', className="container")
])

# Update the `content` div with the `layout` object.
# When you save this file, `debug=True` will re-run
# this script, serving the new layout
# https://community.plot.ly/t/is-there-an-interactive-development-environment-for-dash/7151/2
@app.callback(
    Output('content', 'children'),
    events=[Event('refresh', 'interval')])
def display_layout():
    return layout

if __name__ == '__main__':
    app.run_server(debug=True)