import datetime, time

import pandas as pd
import numpy as np
import dash
from dash import Dash, html, dcc, ctx, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import pandas as pd
import plotly.graph_objects as go

from .side_bar import sidebar
from .def_symbols_tv import get_symbol_names, TIMEFRAMES, TIMEFRAME_DICT
from .vhf_chart_tv import get_data, deleter, adder, jump, vertical_horizontal_indicator, get_vhf_data, vhf_levels, vhf_plot, price_chart

dash.register_page(__name__, name='Trading Dashboard')

symbol_dropdown = html.Div([
    html.P('Symbol:'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': symbol, 'value': symbol} for symbol in get_symbol_names()],
        value='EURUSD',

    )
])

timeframe_dropdown = html.Div([
    html.P('Timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAMES],
        value='M15',
    )
])

slow_ema_input = html.Div([
    html.P('Slow EMA'),
    dbc.Input(id='slow_ema', type='number', value='200')
])

fast_ema_input = html.Div([
    html.P('Fast EMA'),
    dbc.Input(id='fast_ema', type='number', value='55')
])
def layout():
    return html.Div([
    dbc.Row([
            dbc.Col([
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.Div([
                        html.Div([
                            html.Div([
                                # html.Img(src='data:image/png;base64,{}'.format(test_base64),
                                # style={'height':'25%', 'width':'25%'}),
                                html.H1('Trading Dashboard',
                                        style={'margin-top': '60px',
                                               'margin-left': '120px',
                                               'text-align': 'right'}),
                                # theme_switch,
                                # html.P('A dashboard of trading sessions represented as candles',
                                # style={'margin-top': '-8px','text-align': 'center', 'width': '2'})
                            ], style={
                                'display': 'flex',
                                'flex-direction': 'row',
                                'text-align': 'center'
                            }),

                            # html.Hr(),

                            dcc.Interval(id='update', interval=2000),
                            html.Div([
                                html.Div(id='page-content',
                                         style={  # 'border': '1px solid red',
                                             'width': '160vh',
                                             'height': '80vh',
                                             'margin-left': '50px',
                                             'margin-right': '10px',

                                         }),

                                html.Div([
                                    html.Div([
                                        dbc.Col(symbol_dropdown),
                                        dbc.Col(timeframe_dropdown),
                                        dbc.Col(slow_ema_input),
                                        dbc.Col(fast_ema_input),

                                        html.Hr(),

                                    ], style={
                                        'margin-top': '20px',
                                        # 'margin-bottom': '20px',
                                        'margin-left': '50px',
                                        'align': 'center',
                                        # 'border': '1px solid red',
                                        'width': '25vh',
                                        # 'height' : '80vh',
                                    }),

                                ],
                                    style={
                                        # 'border': '1px solid red',
                                        'width': '40vh',
                                        'height': '80vh',
                                    }, id='side-panel'),

                            ], style={
                                # 'border': '1px solid red',
                                # 'width' : '40vh',
                                # 'height' : '80vh',
                                'display': 'flex',
                                'flex-direction': 'row', }),

                            html.Hr(),

                        ], style={
                            # 'border': '1px solid red',
                            # 'width' : '40vh',
                            'height': '120vh',
                            # 'display': 'flex',
                            # 'flex-direction': 'row',
                        })

                    ], style={"height": "800px"})  # "overflow": "scroll"
            ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
])
#])

# @callback(
#     Output('page-content', 'children'),
#     Input('update', 'n_intervals'),
#     State('symbol-dropdown', 'value'), #State('num-bar-input', 'value'),
#     State('timeframe-dropdown', 'value'),
#     State('slow_ema', 'value'), State('fast_ema', 'value')
# )
# def update_ohlc_chart(interval, symbol, timeframe, ema_slow, ema_fast): #, symbol, num_bars, timeframe, ema_slow, ema_fast):
#     timeframe_str = timeframe
#     timeframe = TIMEFRAME_DICT[timeframe]
#     #num_bars = int(num_bars)
#     ema_slow = int(ema_slow)
#     ema_fast = int(ema_fast)
#
#     fig = price_chart(symbol, timeframe, ema_slow, ema_fast)
#
#     return [
#         html.H2(id='chart-details', children= f'{symbol} {timeframe_str}' ), #"Trading View"
#         dcc.Graph(figure=fig, config={'displayModeBar': False}),
#         #dcc.Graph(figure=fig2, config={'displayModeBar': False})
#         ]