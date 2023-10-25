import pandas as pd
import numpy as np
from arch import arch_model
import dash
from dash import Dash, html, dcc, ctx, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_loading_spinners as dls

from .def_symbols_tv import get_symbol_names, TIMEFRAMES, TIMEFRAME_DICT
from .GARCH import get_data, chart_data, diagnostics, forecast, fig_to_uri, model_selection, distribution

from .side_bar import sidebar

dash.register_page(__name__,  order=2, name='GARCH')

# Define the GARCH parameters options
garch_p_options = [{'label': str(i), 'value': i} for i in range(0, 10)]
garch_q_options = [{'label': str(i), 'value': i} for i in range(0, 10)]

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Price Chart", tab_id="chartg"),
                dbc.Tab(label="Distribution Type", tab_id="dist-type"),
                dbc.Tab(label="Model Selection", tab_id="model-selectiong"),
                dbc.Tab(label="Model Diagnostics", tab_id="model-diagnosticsg"),  # model-diagnostics
                dbc.Tab(label="Model Forecast", tab_id="model-forecastg"),
            ],
            id="tabsg",
            # active_tab="chart",
        ),

        html.Br(),

        dls.Hash(html.Div(id="chart-contentg"),
                 color="#435278",
                 speed_multiplier=2,
                 size=50, ),
    ]
)


def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.H3("GENERALIZED AUTOREGRESSIVE CONDITIONAL HETEROSKEDASTICITY"),
                    html.P('GARCH (Generalized Autoregressive Conditional Heteroskedasticity) model is a statistical '
                           'time series model used to analyze and forecast the volatility of financial assets. '
                           , style={'textAlign': 'left'}),

                    dcc.Markdown('''
                                    The key components of the GARCH model are as follows:
                                    * Mean Equation: The mean equation is often modeled as an autoregressive (AR) 
                                        values. process, capturing the linear relationship of the time series with its   
                                        past. It is used to model the mean or expected value of the series.
                                    * Volatility Equation: The volatility equation models the conditional variance of 
                                        the time series. It combines lagged conditional variances (from the ARCH model) 
                                         and lagged squared returns to capture the time-varying nature of volatility.
                                    ''', style={'textAlign': 'left'}),
                    html.P('The GARCH(p, q) model is denoted by specifying the orders of the autoregressive and moving '
                           'average terms in the volatility equation. "p" represents the number of lagged conditional '
                           'variances, and "q" represents the number of lagged squared returns included in the model. '
                           , style={'textAlign': 'left'}),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Ticker Symbol:"),
                                    dcc.Dropdown(
                                        id="symbol-dropdowng",
                                        options=[{'label': symbol, 'value': symbol} for symbol in get_symbol_names()],
                                        value='EURUSD',
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Select Timeframe:"),
                                    dcc.Dropdown(
                                        id="timeframe-dropdowng",
                                        options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAMES],
                                        value='H1',
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                [
                                    html.Label("'p' Parameter:"),
                                    dcc.Dropdown(
                                        id="garch-p-dropdown",
                                        options=garch_p_options,
                                        value=1,
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                [
                                    html.Label("'q' Parameter:"),
                                    dcc.Dropdown(
                                        id="garch-q-dropdown",
                                        options=garch_q_options,
                                        value=1,
                                    ),
                                ],
                                md=2,
                            ),

                            dbc.Col(
                                [
                                    html.Label("Test Data Split:"),
                                    dbc.Input(id='split-input', type='number',
                                              min=5, max=150,
                                              value='100',
                                              ),
                                ],
                                md=2,
                            ),

                            dbc.Col(
                                [
                                    html.Label("Distribution Type:"),
                                    dcc.Dropdown(
                                        id="dist-type",
                                        options=['Normal', 'StudentsT'],
                                        value='Normal',
                                    ),
                                ],
                                md=2,
                            ),
                        ],
                        className='align-items-end', justify='center',
                    ),
                    html.Br(),
                    dbc.Row([
                        html.Div(
                            [
                                dbc.Button(
                                    "Run Model", id="run-buttong", className="me-2", n_clicks=0,
                                    style={'align':'center'}
                                )
                            ]
                        )
                    ]),
                    html.Br(),
                    dbc.Row(
                        [tabs,
                         # dcc.Store inside the user's current browser session
                         dcc.Store(id='train_storeg', data=[], storage_type='session'),
                         # 'local' or 'session' or 'memory'
                         dcc.Store(id='test_storeg', data=[], storage_type='session'),
                         # 'local' or 'session' or 'memory'
                         ]
                    ),
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3'
            )]
        )], fluid=True, class_name='g-0') #p-4

@callback(
    Output('train_storeg', 'data'),
    Output('test_storeg', 'data'),
    Input('symbol-dropdowng', 'value'),
    Input('timeframe-dropdowng', 'value'),
    Input('split-input', 'value'),
    Input('garch-p-dropdown', 'value'),
    Input('garch-q-dropdown', 'value'),
    Input('run-buttong', 'n_clicks'),
    prevent_initial_call = True

)
def data_store(symbol, timeframe, split, p, q, n_clicks):
    if "run-buttong" == ctx.triggered_id:

        train_data, test_data, price_chart = chart_data(str(symbol), str(timeframe), split=int(split), diff=True,
                                                        log=True)
        # print(f'storing train_data to store {train_data}')

        return train_data.to_dict('records'), test_data.to_dict('records'),

    else:
        train_data, test_data, price_chart = chart_data(str(symbol), str(timeframe), split=int(split), diff=True,
                                                        log=True)
        # print(f'storing train_data to store {train_data}')

        return train_data.to_dict('records'), test_data.to_dict('records'),


@callback(
    Output("chart-contentg", "children"),
    # Output('price-plot-div', 'src'),
    Input("tabsg", "active_tab"),
    Input('train_storeg', 'data'),
    Input('test_storeg', 'data'),
    Input('symbol-dropdowng', 'value'),
    Input('timeframe-dropdowng', 'value'),
    Input('split-input', 'value'),
    Input('garch-p-dropdown', 'value'),
    Input('garch-q-dropdown', 'value'),
    Input('dist-type', 'value'),
    Input('run-buttong', 'n_clicks'),
    prevent_initial_call=True

)


def Run_model(tab, train_data, test_data, symbol, timeframe, split, p, q, dist, n_clicks):  # ,

    # if "run-button" == ctx.triggered_id:
    train_data = pd.DataFrame(train_data)
    print(f'test_data - {test_data}')
    test_data = pd.DataFrame(test_data)
    # print(train_data)
    model, summary = model_selection(train_data, p, q, dist='Normal')

    split = int(split)
    symbol = str(symbol)
    timeframe = str(timeframe)

    if tab == "chartg":

        tr_data, te_data, price_chart = chart_data(symbol, timeframe, split=split)

        return html.Div([html.Img(id='price_plot', src=price_chart)],
                        id='price-plot-div')  # , price_chart

    elif tab == "dist-type":

        dist_fig = distribution(train_data, symbol, timeframe)

        return html.Div([html.P('Select Distribution type based on the image below', style={'whiteSpace': 'pre-wrap'}),
                         html.Img(id='price_plot', src=dist_fig)],
                        id='price-plot-div')  # , price_chart

    elif tab == "model-selectiong":

        return html.Div(
            [
                html.P(children=str(summary), style={'whiteSpace': 'pre-wrap'})

            ], id='model_selection-div')  # , price_chart

    elif tab == "model-diagnosticsg":

        dig = diagnostics(train_data, model)
        return html.Div([html.Img(id='diagnostics', src=dig)],
                        id='dig-div')  # , price_chart

    elif tab == "model-forecastg":
        fore = forecast(model, train_data, test_data, symbol, timeframe, split=split)

        return html.Div([html.Img(id='forecast', src=fore)],
                        id='forecast-div')  # , price_chart