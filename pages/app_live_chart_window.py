import warnings
warnings.filterwarnings('ignore')

import dash
from dash import Dash, html, dcc, ctx, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_loading_spinners as dls

from pages.def_symbols_tv import get_symbol_names, TIMEFRAMES_live, TIMEFRAME_DICT
from pages.side_bar import sidebar
from pages.vhf_chart_tv_white import price_chart, calc_lot_size

dash.register_page(__name__,  order=3, name='Live Chart + Lotsize Calculator') #3 is now used

symbol_dropdown = html.Div([
    # html.P('Symbol:'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': html.Span([symbol], style={'color': 'Black'}), 'value': symbol} for symbol in
                 get_symbol_names()],
        value='EURUSD',

    )
])

slow_ema_input = html.Div([
    html.P('Slow EMA'),
    dbc.Input(id='slow_ema', type='number', min=10, max=200, value='200')
])

fast_ema_input = html.Div([
    html.P('Fast EMA'),
    dbc.Input(id='fast_ema', type='number', min=10, max=200, value='55')
])

account_currency = html.Div([
    html.P('Account Currency'),
    dbc.Input(id='account-currency', type='text', placeholder="USD", value='USD')
], className="P-2")

account_balance = html.Div([
    html.P('Account Balance'),
    dbc.Input(id='account-balance', type='number', min=10, value=10000)
], className="P-2")

risk = html.Div([
    html.P('Risk Amount'),
    dbc.Input(id='risk', type='number', min=0.01, max=99.9, value=1)
], className="P-2")

stop_loss = html.Div([
    html.P('StopLoss (Points)'),
    dbc.Input(id='stop-loss', type='number', min=10, value=100, step=1)
], className="P-2")

button = html.Div(
    [
        dbc.Button(
            "Calculate LotSize", id="lot-button", className="me-2", n_clicks=0
        )
    ], className="P-2"
)

timeframe_group = html.Div(
    [
        dbc.RadioItems(
            id="timeframe-radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAMES_live],
            value='D1',
        ),
        # html.Div(id="output"),
    ],
    className="radio-group",
)

candle_group = html.Div(
    [
        dbc.RadioItems(
            id="candle-radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[{'label': 'Candles', 'value': 'candle'},
                     {'label': 'Line', 'value': 'line'}],
            value='candle',
        ),
        # html.Div(id="output"),
    ],
    className="radio-group",
)
def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            dbc.Col([
                # dbc.Container(
                #     children=[
                    # Headers
                    dbc.Row([
                        # heading title
                        dbc.Col([
                            html.H2('TRADING DASHBOARD', className='text-center p-6', style={"color": 'white'}),
                            html.H4('A simple Live Chart and a Lotsize Calculator', className='text-center p-6', style={"color": 'white'}),
                        ],  # width=6
                            #xs=8, sm=8, md=10, lg=10, xl=10, align='left',
                            className='p-3'),

                        # dbc.Col([
                        #     # theme_switch,
                        # ]),

                    ], justify='center', style={"height": "10%"}),

                    dcc.Interval(id='update', interval=5000),

                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Symbol'),
                            symbol_dropdown,
                        ], xs=1, sm=1, md=1, lg=1, xl=1, className='p-3'),
                        dbc.Col([
                            html.Label('Timeframes'),
                            timeframe_group,
                        ], xs=1, sm=1, md=1, lg=3, xl=3, className='p-3'),

                        dbc.Col([
                            html.Label('Candle Type'),
                            candle_group,
                        ], xs=1, sm=1, md=3, lg=3, xl=3, className='p-3'),

                        dbc.Col([
                            # fast_ema_input,
                        ], xs=1, sm=1, md=1, lg=1, xl=1, className='p-3'),

                    ], justify='center', className='align-items-end', #style={"height": "5%"}
                        ),

                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.H2(children=[], id='chart-details'),
                            # dls.Hash(html.Div(html.H2(children=[]), id='chart-details'),
                            #                  color="#435278",
                            #                 speed_multiplier=2,
                            #                 size=25,),
                            html.Div([dcc.Graph(figure=[])], id='chart'),

                        ], width=10, className='p-1'),

                        dbc.Col([
                            dbc.Row([
                                html.H4('Indicators:'),
                                slow_ema_input,
                                html.Br(),
                                fast_ema_input
                            ]),

                            html.Hr(),
                            dbc.Row([
                                html.H4('Lot Size Calculator:'),
                                account_currency,
                                account_balance,
                                risk,
                                stop_loss,
                                button,

                                # html.Div(id='lotsize-output', className='p-3')
                                dls.Hash(html.Div(id='lotsize-output', className='p-3'),
                                                                 color="#435278",
                                                                speed_multiplier=2 ,
                                                                size=25)
                            ])
                        ], width=2, className='p-1')

                    ], justify='left', className='p-3', style={"height": "70%"})

                #], style={"margin": "30 auto", "height": "99vh"})  # class_name='border g-0 p-4 vh-100')
            ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3')
        ])
    ], fluid=True, class_name='g-0') # p-6
        #style={'background-size': '100%'})  # "height": "99vh",


@callback(
    Output('chart', 'children'),
    Output('chart-details', 'children'),
    Input('update', 'n_intervals'),
    Input('symbol-dropdown', 'value'),  # State('num-bar-input', 'value'),
    Input('timeframe-radios', 'value'),
    Input('candle-radios', 'value'),
    State('slow_ema', 'value'), State('fast_ema', 'value')
)
def update_ohlc_chart(interval, symbol, timeframe, plot_type, ema_slow, ema_fast):#, ema_slow, ema_fast):
    timeframe_str = timeframe
    timeframe = TIMEFRAME_DICT[timeframe]
    ema_slow = int(ema_slow)
    ema_fast = int(ema_fast)

    fig = price_chart(symbol, timeframe, ema_slow, ema_fast, plot_type)

    return dcc.Graph(figure=fig, config={'displayModeBar': False}), html.H2(id='chart-details', children=f'{symbol} {timeframe_str}')

@callback(
    Output('lotsize-output', 'children'),
    Input('lot-button', 'n_clicks'),
    Input('symbol-dropdown', 'value'),  # State('num-bar-input', 'value'),
    Input('account-currency', 'value'),
    Input('account-balance', 'value'),
    Input('risk', 'value'),
    Input('stop-loss', 'value'),
)

def lotsize_calc(n_clicks, symbol, account_c, account_b, risk, sl):
    #if n_clicks is None:
    if 'lot-button' == ctx.triggered_id:
        lotsize = calc_lot_size(symbol, account_c, account_b, risk, sl)
        return html.H5(children=f'Lot Size: {lotsize}')

    else:
        raise PreventUpdate