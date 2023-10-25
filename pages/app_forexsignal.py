import dash
from dash import Dash, html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from .def_symbols import get_symbol_names, TIMEFRAMES
from .TradingViewTA import forex_scaner
from .side_bar import sidebar

dash.register_page(__name__, order=3, name='Forex Trading Signals')

timeframe_dropdown = html.Div([
    html.P('Select Timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAMES],
        value='D1',
    )
],
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
                    dbc.Container(
                        children=[
                            dbc.Row([
                                html.H3(children='FOREX Trading Signals',
                                        style={'text-align': 'center'}
                                        ),
                                html.P(
                                    'This is a simple FOREX signal app which pulls signals of FOREX pairs from TradingView. '
                                    'Select a timeframe, Click Fetch and have a look at your chart! '
                                    , style={'textAlign': 'left'}),
                            ], style={'align': 'center'}),  # , className='border'),

                            html.Hr(),
                            dbc.Row([

                                dbc.Col([

                                    html.Div([
                                        timeframe_dropdown,
                                        html.Br(),
                                        dbc.Button("Fetch", id="refresh", n_clicks=0, className="me-2"),
                                    ], style={'align': 'center'}),

                                    html.Hr(),

                                    dbc.Row([

                                        dls.Hash(html.Div(id='signal-table-div',
                                                          style={'width':'100%', "height": "65vh"},
                                                          className="overflow-auto"),
                                                 color="white",
                                                 speed_multiplier=5,
                                                 size=40, )
                                    ])

                                ], width={"size": 6, "offset": 3}, style={'align': 'center'})

                            ]),
                        ], style={"margin": "30 auto", "height": "99vh"})  # class_name='border g-0 p-4 vh-100')

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3')
        ]
    )], fluid=True, class_name='g-0 vh-100', )  # p-4


@callback(Output('signal-table-div', 'children'),
          Input('refresh', 'n_clicks'),
          State('timeframe-dropdown', 'value'),
          prevent_initial_call=True
          )
def update_table(n_click, timeframe):
    if n_click:
        symbols = get_symbol_names()
        data = forex_scaner(symbols, timeframe)
        data = data.reset_index()
        data.columns = ['Symbols', 'Signal']

        table = dash_table.DataTable(
            data.to_dict('records'), [{"name": i, "id": i} for i in data.columns],
            id='signal-table',
            style_cell={
                'textAlign': 'center',
                'backgroundColor': '#f4f4f4'
            },
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{Signal} contains "SELL"',
                        'column_id': 'Signal'
                    },
                    'backgroundColor': 'red',
                    'color': 'white'
                },

                {
                    'if': {
                        'filter_query': '{Signal} contains "BUY"',
                        'column_id': 'Signal'
                    },
                    'backgroundColor': 'green',
                    'color': 'white'
                },
                #                             {
                #                             'if': {
                #                                 'filter_query': '{Signal} contains "SELL"'
                #                             },
                #                             'color': 'red'
                #                         },

                #                                 {
                #                             'if': {
                #                                 'filter_query': '{Signal} contains "BUY"'
                #                             },
                #                             'color': 'green'
                #                         },

                {
                    'if': {
                        'filter_query': '{Signal} contains "NEUTRAL"'
                    },
                    'color': 'white'
                }

            ]
        )
    else:
        raise PreventUpdate
    return table