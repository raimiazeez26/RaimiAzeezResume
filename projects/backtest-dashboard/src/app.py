from Backtests import get_data, signal, Strategy, Position, calc_metrics
import quantstats as qs

# extend pandas functionality with metrics, etc.
qs.extend_pandas()
import dash
from dash import Dash, html, dcc, dash_table, ctx, clientside_callback
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
import dash_ag_grid as dag
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime, timedelta

from ta import add_all_ta_features
pd.options.display.float_format = '{:.3f}'.format


def run_backtest(ticker, timeframe, buy_con_type, buy_con, buy_ind1, buy_ind2, sell_con_type, sell_con, sell_ind1,
                 sell_ind2, sl, tp):
    EXCHANGE = 'OANDA'
    df_backtest = get_data(ticker, timeframe, EXCHANGE)
    df_backtest = add_all_ta_features(df_backtest, open='Open', high='High', low='Low', close='Close', volume='Volume')
    df_backtest = signal(df_backtest, buy_con_type, buy_con, buy_ind1, buy_ind2, sell_con_type, sell_con, sell_ind1,
                         sell_ind2)

    starting_balance = 100000
    sl_pips = sl
    tp_pips = tp

    strategy = Strategy(df_backtest, starting_balance, sl_pips, tp_pips)
    result = strategy.run()
    result["Ticker"] = ticker

    return [result, df_backtest]


symbol_list = ["EURCAD", "AUDUSD", "USDCAD", "USDCHF", "AUDCAD", "CADCHF", "NZDUSD", "EURCAD", "AUDCHF", "GBPUSD",
               "GBPCAD", "GBPNZD", "AUDNZD", "EURGBP", "EURNZD", "GBPCHF", "EURCHF", "EURAUD", "NZDCAD", "NZDCHF",
               "GBPAUD"]

TIMEFRAMES = ['M1', 'M5', 'M15', 'M30', 'M45', 'H1', 'H4', 'D1', 'W1', 'MN1']

indicator_list = ['Open', 'Close', 'Low', 'High', 'volume_adi', 'volume_obv', 'volume_cmf', 'volume_fi', 'volume_em',
                  'volume_sma_em', 'volume_vpt', 'volume_vwap', 'volume_mfi',
                  'volume_nvi', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl',
                  'volatility_bbw', 'volatility_bbp', 'volatility_bbhi',
                  'volatility_bbli', 'volatility_kcc', 'volatility_kch', 'volatility_kcl',
                  'volatility_kcw', 'volatility_kcp', 'volatility_kchi',
                  'volatility_kcli', 'volatility_dcl', 'volatility_dch', 'volatility_dcm',
                  'volatility_dcw', 'volatility_dcp', 'volatility_atr', 'volatility_ui',
                  'trend_macd', 'trend_macd_signal', 'trend_macd_diff', 'trend_sma_fast',
                  'trend_sma_slow', 'trend_ema_fast', 'trend_ema_slow',
                  'trend_vortex_ind_pos', 'trend_vortex_ind_neg', 'trend_vortex_ind_diff',
                  'trend_trix', 'trend_mass_index', 'trend_dpo', 'trend_kst',
                  'trend_kst_sig', 'trend_kst_diff', 'trend_ichimoku_conv',
                  'trend_ichimoku_base', 'trend_ichimoku_a', 'trend_ichimoku_b',
                  'trend_stc', 'trend_adx', 'trend_adx_pos', 'trend_adx_neg', 'trend_cci',
                  'trend_visual_ichimoku_a', 'trend_visual_ichimoku_b', 'trend_aroon_up',
                  'trend_aroon_down', 'trend_aroon_ind', 'trend_psar_up',
                  'trend_psar_down', 'trend_psar_up_indicator',
                  'trend_psar_down_indicator', 'momentum_rsi', 'momentum_stoch_rsi',
                  'momentum_stoch_rsi_k', 'momentum_stoch_rsi_d', 'momentum_tsi',
                  'momentum_uo', 'momentum_stoch', 'momentum_stoch_signal', 'momentum_wr',
                  'momentum_ao', 'momentum_roc', 'momentum_ppo', 'momentum_ppo_signal',
                  'momentum_ppo_hist', 'momentum_pvo', 'momentum_pvo_signal',
                  'momentum_pvo_hist', 'momentum_kama']

graph_style = {"height": '100%', 'border-radius': '13px',
               'background': '#FFFFFF 0% 0% no-repeat padding-box',  ##FFFFFF
               'border': '1px solid  #CECECE',
               'box-shadow': '3px 3px 6px #00000029', 'padding': '3px',
               'font-size': '16vmin'}
col_style = {'background': '#FFFFFF 0% 0% no-repeat padding-box',
             'border-radius': '13px',
             'border': '1px solid  #CECECE', 'color': '#2e97a4',
             'box-shadow': '3px 3px 6px #00000029', 'padding': '3px'}
table_style = {"height": '100%', 'border-radius': '13px',
               'background': '#FFFFFF 0% 0% no-repeat padding-box',
               # 'border': '1px solid  #CECECE',
               # 'box-shadow': '3px 3px 6px #00000029', 'padding': '3px',
               'font-size': '1vmin', 'color': '#2e97a4'}


def plot_pnl(df, symbol):
    fig = px.line(df, x="open_datetime", y="pnl", title=f'{symbol} Profit/Loss Chart')
    fig.update_layout(
        #             title= f"{symbol} Chart",
        #             yaxis_title=f"{symbol}",
        margin=dict(l=1, r=1, t=32, b=1), )

    return fig


run_button = html.Div(
    [
        dbc.Button(
            "Run Backtest", id="run-button", className="me-2", n_clicks=0
        )
    ]
)


def calc_metrics(backtest_result):
    returns = backtest_result['returns']
    metric = {
        'Cumulative Returns(%)': returns.compsum().iloc[-1] * 100,
        'CAGR%': returns.cagr() * 100,
        'Win Rate': returns.win_rate() * 100,
        'Win Loss Ratio': returns.win_loss_ratio(),
        'Consecutive Wins': returns.consecutive_wins(),
        'Consecutive Losses': returns.consecutive_losses(),
        'Risk Return Ratio': returns.risk_return_ratio(),
        'Sharpe Ratio': returns.sharpe(),
        'Sortino Ratio': returns.sortino(),
        'Max Drawdown': returns.max_drawdown() * 100,
        #     'Longest DD Days' : returns.sharpe(),
        #     'Average DD' : returns.sharpe(),
        #     'Average DD Days' : returns.sharpe(),
        'Recovery Factor': returns.recovery_factor(),
        'Calmar': returns.calmar(),
        'Skew': returns.skew(),
        'Kurtosis': returns.kurtosis(),
        #     'Expected Daily %' : returns.sharpe(),
        #     'Expected Monthy %' : returns.monthly_returns(),
        #     'Expected Yearly %' : returns.sharpe(),
        'Kelly Criterion': returns.kelly_criterion() * 100,
        'Daily VaR': returns.var() * 100,
        'Profit Factor': returns.profit_factor(),
        'Profit Ratio': returns.profit_ratio(),
        #     'Win Days %' : returns.sharpe(),
        #     'Win Month %' : returns.sharpe(),
        #     'Win Quarter %' : returns.sharpe(),
        #     'Win Year %' : returns.sharpe(),

    }

    metrics = pd.DataFrame.from_dict(metric, orient='index')
    metrics = metrics.reset_index()
    metrics.columns = ['Metrics', 'Values']
    return metrics


# creates the Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE],  # ZEPHYR],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])  # dbc.themes.MINTY

server = app.server

# creates the layout of the App
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('BACKTEST DASHBOARD'),
            html.H5('Select Buy & Sell Conditions, and the backtest parameter, then run backtest. ')
        ], width=8, class_name='p-1 text-center', id='header'),
    ], justify='center', style={"height": "15%"}),

    html.Hr(),

    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.H5("Buy Conditions"),

            ], width=12, class_name='p-1 text-center', ),
        ]),

        dbc.Col([html.Label("Buy Indicator1:"),
                 dcc.Dropdown(
                     id="buy-indicator1",
                     options=[{'label': symbol, 'value': symbol} for symbol in indicator_list],
                     value='trend_ema_fast',
                 )], md=2, ),
        dbc.Col([html.Label("Condition:"),
                 dcc.Dropdown(
                     id="buy-condition-type",
                     options=['equal to', 'greater than', 'less than', 'greater than or equal to',
                              'less than or equal to'],
                     value='greater than',
                 )], md=2, ),
        dbc.Col([html.Label("Buy Indicator 2 Type:"),
                 dcc.Dropdown(
                     id="buy-indicator2-type",
                     options=['Indicator', 'Value'],
                     value='Indicator',
                 )], md=2, ),
        dbc.Col([
        ], md=2, id='indicator2-type-col'),

        #         dbc.Col([
        #                     run_button,
        #                 ], xs=2, sm=2, md=2, lg=2, xl=2),
    ], className='align-items-end, m2', justify='center'),

    html.Hr(),

    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.H5("Sell Conditions"),

            ], width=12, class_name='p-1 text-center', ),
        ]),

        dbc.Col([html.Label("Sell Indicator1:"),
                 dcc.Dropdown(
                     id="sell-indicator1",
                     options=[{'label': symbol, 'value': symbol} for symbol in indicator_list],
                     value='trend_ema_fast',
                 )], md=2, ),
        dbc.Col([html.Label("Condition:"),
                 dcc.Dropdown(
                     id="sell-condition-type",
                     options=['equal to', 'greater than', 'less than', 'greater than or equal to',
                              'less than or equal to'],
                     value='greater than',
                 )], md=2, ),
        dbc.Col([html.Label("Sell Indicator 2 Type:"),
                 dcc.Dropdown(
                     id="sell-indicator2-type",
                     options=['Indicator', 'Value'],
                     value='Indicator',
                 )], md=2, ),
        dbc.Col([
        ], md=2, id='sell-indicator2-type-col'),

        #         dbc.Col([
        #                     run_button,
        #                 ], xs=2, sm=2, md=2, lg=2, xl=2),
    ], className='align-items-end', justify='center'),

    html.Hr(),
    dbc.Row([
        dbc.Col(
            [
                html.Label("Ticker Symbol:"),
                dcc.Dropdown(
                    id="ticker-dropdown",
                    options=[{'label': symbol, 'value': symbol} for symbol in symbol_list],
                    value='GBPUSD',
                ),
            ],
            md=2,
        ),
        dbc.Col(
            [
                html.Label("Select Timeframe:"),
                dcc.Dropdown(
                    id="timeframe-dropdown",
                    options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAMES],
                    value='H1',
                ),
            ],
            md=2,
        ),
        dbc.Col(
            [
                html.Label("Stop Loss(Pips):"),
                dbc.Input(id='stop-loss', type='number', min=1, max=1000,
                          value='10')
            ],
            md=2,
        ),
        dbc.Col(
            [
                html.Label("Take Profit(Pips)"),
                dbc.Input(id='take-profit', type='number', min=1, max=1000,
                          value='50')

            ],
            md=2,
        ),

        dbc.Col([
            run_button,
        ], xs=2, sm=2, md=2, lg=2, xl=2),

    ], className='align-items-end pb-2', justify='center'),
    html.Hr(),
    dls.Hash(dcc.Store(id='result-store'),
             color="#435278",
             speed_multiplier=2,
             size=50, ),
    dbc.Row([

        dbc.Col([
            #             dcc.Graph(figure= plot_fig(data, date=None), style=graph_style, config={'displayModeBar': False})
        ],
            width=10, class_name='p-1', id='chart'),  # plot_fig(symbol, df)

    ], justify='center', style={"height": "40%"}),  # , "background-color": "cyan"
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dls.Hash(html.Div(
                # [html.H3('AMOTIZATION SCHEDULE', style={'textAlign': 'center'}),
                # table
                # ],
                id='result-table'),
                color="#435278",
                speed_multiplier=2,
                size=50, ),

        ]),
    ], justify='center', class_name='g-0 p-4'),  # style={"height": "50%"}), #, "background-color": "cyan"

    html.Hr(),

    dbc.Row([
        dbc.Col([
            dls.Hash(html.Div(
                # [html.H3('AMOTIZATION SCHEDULE', style={'textAlign': 'center'}),
                # table
                # ],
                id='metric-table'),
                color="#435278",
                speed_multiplier=2,
                size=50, ),

        ], width=6),
    ], justify='center', class_name='g-0 p-4'),  # style={"height": "50%"}), #, "background-color": "cyan"
    # dcc.Store stores the intermediate value
    dcc.Store(id='result-store2'),

], fluid=True, class_name='g-0 p-4')  # , style={"height": "200vh", 'background-size': '200%'}) #fluid = True,


@app.callback(
    Output('result-store', 'data'),
    Output('result-store2', 'data'),
    #               Output('retult-table', 'children'), #, allow_duplicate = True),
    Input('run-button', 'n_clicks'),
    #               Input('result-store', 'data'),
    #               Input('result-table', 'cellClicked'),
    Input('ticker-dropdown', 'value'),
    Input('timeframe-dropdown', 'value'),
    Input('buy-indicator2-type', 'value'),
    Input('buy-condition-type', 'value'),
    Input('buy-indicator1', 'value'),
    Input('buy-indicator2', 'value'),
    Input('sell-indicator2-type', 'value'),
    Input('sell-condition-type', 'value'),
    Input('sell-indicator1', 'value'),
    Input('sell-indicator2', 'value'),
    Input('stop-loss', 'value'),
    Input('take-profit', 'value'),

    #               prevent_initial_call = True
)
def update_b_results(n_clicks, ticker, timeframe, buy_con_type, buy_con, buy_ind1, buy_ind2, sell_con_type, sell_con,
                     sell_ind1, sell_ind2, sl, tp):
    if "run-button" == ctx.triggered_id:
        print('button clicked')

        data = run_backtest(ticker, timeframe, buy_con_type, buy_con, buy_ind1, buy_ind2, sell_con_type, sell_con,
                            sell_ind1, sell_ind2, float(sl), float(tp))
        #         data = pd.read_json(data, orient='split')
        #         print(data)

        return [data[0].to_json(date_format='iso', orient='split'), data[1].to_json(date_format='iso', orient='split')]
    else:
        print('button not clicked')
        raise PreventUpdate


@app.callback(Output('result-table', 'children'),
              Input('result-store', 'data'),
              # Input('result-store2', 'data'),
              )
def backtest_result_data(data):
    if data is not None:
        print('data loaded')
        data = pd.read_json(data, orient='split')
        data['open_datetime'] = pd.to_datetime(data['open_datetime'])
        #         tick_data = pd.read_json(tick_data, orient='split')

        # create a number-based filter for columns with integer data
        col_defs = []
        for i in data.columns:
            col_defs.append({"field": i})

        table = [
            html.H5('BACKTEST RESULTS',
                    style={'textAlign': 'center'}),
            html.Button("Export to CSV", id="btn-csv"),
            dag.AgGrid(
                id="result-table",
                rowData=data.to_dict("records"),
                columnDefs=col_defs,
                defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth": 115},
                columnSize="sizeToFit",
                #                 dashGridOptions={"pagination": True, "paginationPageSize":10},
                #                 dashGridOptions={
                #                     "excelStyles": excelStyles,
                #                     },
                csvExportParams={
                    "fileName": "backtest_result.csv",
                },
                enableEnterpriseModules=True,
                className="ag-theme-alpine",
            )]

        return table
    else:
        print('Data is None')
        raise PreventUpdate


@app.callback(Output('metric-table', 'children'),
              Input('result-store', 'data'),
              )
def metrics_data(data):
    if data is not None:
        print('data loaded')
        data = pd.read_json(data, orient='split')
        data['open_datetime'] = pd.to_datetime(data['open_datetime'])
        data.set_index('open_datetime', inplace=True)
        data = calc_metrics(data).round(3)

        # create a number-based filter for columns with integer data
        col_defs = []
        for i in data.columns:
            col_defs.append({"field": i})

        table = [
            html.H5('BACKTEST METRICS',
                    style={'textAlign': 'center'}),
            html.Button("Export to CSV", id="btn-csv"),
            dag.AgGrid(
                id="metrics-table",
                rowData=data.to_dict("records"),
                columnDefs=col_defs,
                defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth": 115},
                columnSize="sizeToFit",
                #                 dashGridOptions={"pagination": True, "paginationPageSize":10},
                #                 dashGridOptions={
                #                     "excelStyles": excelStyles,
                #                     },
                csvExportParams={
                    "fileName": "backtest_metrics.csv",
                },
                enableEnterpriseModules=True,
                className="ag-theme-alpine",
            )]

        return table
    else:
        print('Data is None')
        raise PreventUpdate


@app.callback(
    Output('chart', 'children'),
    Input('result-store', 'data'),
    Input('result-store2', 'data'),
    Input('result-table', 'cellClicked'),
    Input('timeframe-dropdown', 'value'),
    Input('ticker-dropdown', 'value'),
)
def update_graph(data, tick_data, cell_clicked, timeframe, symbol):
    if data is not None:
        print('data loaded')
        data = pd.read_json(data, orient='split')
        data['open_datetime'] = pd.to_datetime(data['open_datetime'])
        tick_data = pd.read_json(tick_data, orient='split')

        if cell_clicked:

            datetime = data.loc[cell_clicked['rowIndex'], cell_clicked['colId']]
            print(datetime)
            date = datetime.date()

            if timeframe == 'D1' or timeframe == 'H4':
                start_date = date - timedelta(days=30)
                end_date = date + timedelta(days=30)

            elif timeframe == 'H1' or timeframe == 'M30':
                start_date = date - timedelta(weeks=1)
                end_date = date + timedelta(weeks=1)

            else:
                start_date = date - timedelta(hours=10)
                end_date = date + timedelta(hours=10)

            tick_data['date'] = [i.date() for i in tick_data['datetime']]
            df_an = tick_data[tick_data['date'] >= start_date]
            df_an = df_an[df_an['date'] <= end_date]
            chart = dcc.Graph(figure=plot_pnl(data, symbol), style=graph_style,
                              config={'displayModeBar': False})  # plot_fig(df_an, symbol, date)

            return chart

        else:
            chart = dcc.Graph(figure=plot_pnl(data, symbol), style=graph_style, config={'displayModeBar': False})
            return chart
    else:
        #         print('Data is None')
        raise PreventUpdate


@app.callback(
    Output("result-table", "exportDataAsCsv"),
    Input("btn-csv", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False


@app.callback(Output('indicator2-type-col', 'children'),
              Output('sell-indicator2-type-col', 'children'),
              #           Input('buy-condition-type', 'value'),
              Input('buy-indicator2-type', 'value'),
              Input('sell-indicator2-type', 'value'),
              )
def indicator_type(buy_ind2_type, sell_ind2_type):
    if buy_ind2_type == 'Indicator':
        ind2 = html.Div([
            html.Label("Buy Indicator2:"),
            dcc.Dropdown(
                id="buy-indicator2",
                options=[{'label': symbol, 'value': symbol} for symbol in indicator_list],
                value='trend_ema_slow')
        ])
    else:
        ind2 = html.Div([
            html.Label("Buy Indicator2:"),
            dbc.Input(id='buy-indicator2', type='number', min=1, max=100,
                      value='10')
        ])

    if sell_ind2_type == 'Indicator':
        sell_ind2 = html.Div([
            html.Label("Sell Indicator2:"),
            dcc.Dropdown(
                id="sell-indicator2",
                options=[{'label': symbol, 'value': symbol} for symbol in indicator_list],
                value='trend_ema_slow')
        ])
    else:
        sell_ind2 = html.Div([
            html.Label("Sell Indicator2:"),
            dbc.Input(id='sell-indicator2', type='number', min=1, max=100,
                      value='10')
        ])

    return [ind2, sell_ind2]


if __name__ == '__main__':
    # starts the server
    app.run_server()
