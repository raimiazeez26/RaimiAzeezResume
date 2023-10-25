import datetime, time
import pandas as pd
import numpy as np
import dash
from dash import Dash, html, dcc, ctx, callback
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
from dash.exceptions import PreventUpdate

from .side_bar import sidebar
from .def_symbols_tv import get_symbol_names, TIMEFRAMES, TIMEFRAME_DICT
from .main_arima import get_data, chart_data, acf_pcf, model_selection, diagnostics, forecast, forecast_log, fig_to_uri

dash.register_page(__name__,  order=1, name='ARIMA')

# creates the Dash App
#app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

##=========================================================================================================
#Inputs parameters
##=========================================================================================================

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
        value='H1',
    )
])

log_check = dbc.Checkbox(
            id="log-checkbox",
            label="Log of Price",
            value=False,
        )

diff_check = dbc.Checkbox(
            id="diff-checkbox",
            label="First Difference",
            value=False,
        )

split = html.Div([
    html.P('Test Data Split'),
    dbc.Input(id='split', type='number', min = 5, max = 150,
              value='100')
])

run_button = html.Div(
    [
        dbc.Button(
            "Run Model", id="run-button", className="me-2", n_clicks=0
        )
    ]
)

##=========================================================================================================

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Price Chart", tab_id="chart"),
                dbc.Tab(label="ACF/PACF", tab_id="acf_pacf"),
                dbc.Tab(label="Model Selection", tab_id="model-selection"),
                dbc.Tab(label="Model Diagnostics", tab_id="model-diagnostics"), #model-diagnostics
                dbc.Tab(label="Model Forecast", tab_id="model-forecast"),
            ],
            id="tabs",
            active_tab="chart",
        ),
        
        html.Br(),
        
       dls.Hash(html.Div(id="chart-content"),
                color="#435278",
                speed_multiplier=2,
                size=50,),
    ]
)



def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2,
            ),

            dbc.Col(
                [
                    html.H3('AUTOREGRESSIVE INTEGRATED MOVING AVERAGE MODEL (ARIMA)', style={'textAlign':'center'}, className='p4'),
                    html.P('ARIMA is a popular time series forecasting model. ARIMA model incorporates three components:'
                           , style={'textAlign': 'left'}),

                    dcc.Markdown('''
                            * Autoregressive (AR) Component: This component captures the linear relationship between an 
                                observation and a lagged value(s) of the time series. The "p" parameter determines the 
                                number of lagged terms used in the model.
                            * Moving Average (MA) Component: This component represents the dependency between an 
                                observation and residual errors from past observations. The "q" parameter determines 
                                the number of lagged errors used in the model.
                            * Differencing (I) Component: This component is used to transform the time series into a 
                                stationary series by taking the difference between consecutive observations. 
                                The "d" parameter determines the order of differencing required to achieve stationarity.
                            ''', style={'textAlign': 'left'}),

                    html.P('To select the optimal values for the "p", "d", and "q" parameters, we can use the '
                           'Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) plots. '
                           '** Click the Run Model button to start. **'
                           , style={'textAlign': 'left'}),
                    html.Hr(),
                    
                    dbc.Container([
                        
                        #inputs
                        dbc.Row([
                            dbc.Col([
                                    symbol_dropdown,
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),
                                    dbc.Col([
                                        timeframe_dropdown,
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),

                                    dbc.Col([
                                        log_check,
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),

                                    dbc.Col([
                                        diff_check,
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),

                                    dbc.Col([
                                        split,
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),
                            
                                    dbc.Col([
                                        run_button,
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),
                            
                                ], className='align-items-end', justify='center'),
                        
                        html.Br(),
                        html.Hr(),
                        
                        #tabs
                        dbc.Row([
                            tabs,
                            # dcc.Store inside the user's current browser session
                            dcc.Store(id='train_store', data=[], storage_type='session'), # 'local' or 'session' or 'memory'
                            dcc.Store(id='test_store', data=[], storage_type='session'), # 'local' or 'session' or 'memory'
                        ]),
                        
                    ])

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3'
            )
        ]
    )], fluid=True, class_name='g-0',) # p-4
        #style={"height": "99vh", 'background-size': '100%'})

@callback(
    Output('train_store', 'data'),
    Output('test_store', 'data'),
    Input('symbol-dropdown', 'value'),
    Input('timeframe-dropdown', 'value'),
    Input('split', 'value'),
    Input('diff-checkbox', 'value'), 
    Input('log-checkbox', 'value'),
    Input('run-button', 'n_clicks'),
    prevent_initial_call = True
    
)

def data_store(symbol, timeframe, split, diff, log, n_clicks):
    
    if "run-button" == ctx.triggered_id:
    
        train_data, test_data, price_chart = chart_data(symbol, timeframe, split= int(split), diff = diff, log = log)
       # print(f'storing train_data to store {train_data}')

        return train_data.to_dict('records'), test_data.to_dict('records')
    
    else:
        train_data, test_data, price_chart = chart_data(symbol, timeframe, split= int(split), diff = diff, log = log)
        #print(f'storing train_data to store {train_data}')

        return train_data.to_dict('records'), test_data.to_dict('records')


@callback(
    Output("chart-content", "children"), 
    #Output('price-plot-div', 'src'),
    Input("tabs", "active_tab"),
    Input('train_store', 'data'),
    Input('test_store', 'data'),
    Input('symbol-dropdown', 'value'),
    Input('timeframe-dropdown', 'value'),
    Input('split', 'value'),
    Input('diff-checkbox', 'value'), 
    Input('log-checkbox', 'value'),
    Input('run-button', 'n_clicks'),
    prevent_initial_call = True
    
)

def Run_model(tab, train_data, test_data, symbol, timeframe, split, diff, log, n_clicks): #,
    
    #if "run-button" == ctx.triggered_id:
    train_data = pd.DataFrame(train_data)
    test_data = pd.DataFrame(test_data)
    best, model, summary = model_selection(train_data)

    split = int(split)

    #if "run-button" == ctx.triggered_id:
    
    if tab == "chart":

        tr_data, te_data, price_chart = chart_data(symbol, timeframe, split= int(split), diff = diff, log = log)

        return html.Div([html.Img(id = 'price_plot', src = price_chart)],
                         id='price-plot-div') #, price_chart

    elif tab == "acf_pacf":

        acf_pacf = acf_pcf(train_data)
        return html.Div([html.Img(id = 'acf_pacf', src = acf_pacf)],
             id='acf_pacf-div') #, price_chart

    elif tab == "model-selection":

        #model, summary = model_selection(train_data)

        return html.Div(
            [
                html.P(f'Best Model : ARIMA {best}'),
                html.P(children=str(summary), style={'whiteSpace': 'pre-wrap'})

            ],id='model_selection-div') #, price_chart

    elif tab == "model-diagnostics":

        dig = diagnostics(model)
        return html.Div([html.Img(id = 'giagnostics', src = dig)],
             id='dig-div') #, price_chart

    elif tab == "model-forecast":
        if log:
            
            fore = forecast_log(model, train_data, test_data, symbol, timeframe, split=split, alpha1= 0.20, alpha2=0.05)
            return html.Div([html.Img(id = 'forecast', src = fore)],
                 id='forecast-div') #, price_chart
        else:
            fore = forecast(model, train_data, test_data, symbol, timeframe, split=split, alpha1= 0.20, alpha2=0.05)
            return html.Div([html.Img(id = 'forecast', src = fore)],
                 id='forecast-div') #, price_chart
        
    #else:
        #raise PreventUpdate

