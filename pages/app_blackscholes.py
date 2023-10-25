import pandas as pd
import numpy as np
import dash
from dash import Dash, html, dcc, ctx, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
from scipy.stats import norm
from .BlackScholes import BS
from .side_bar import sidebar

dash.register_page(__name__, order=8, name='OPTION PRICING - Black-Scholes Model')

spot_price = html.Div([
    html.P('Spot Price'),
    dbc.Input(id="spot-price", type='number', min = 0.01,
              value=100, placeholder="Spot Price")
])

strike_price = html.Div([
    html.P('Strike Price'),
    dbc.Input(id="strike-price", type='number', min = 0.01,
              value=100, placeholder="Strike Price")
])

maturity = html.Div([
    html.P('Time to Maturity (years'),
    dbc.Input(id="time-to-maturity", type='number',
              value=1, placeholder="Time to Maturity")
])

volatility = html.Div([
    html.P('Volatility'),
    dbc.Input(id="sigma", type='number',
              value=0.20, placeholder="Volatility")
])

interest_rate = html.Div([
    html.P('Interest Rate'),
    dbc.Input(id="interest-rate", type='number',
              value=0.02, placeholder="Interest Rate")
])

cal_button = html.Div(
    [
        dbc.Button(
            "Calculate", id="calculate-button", className="me-2", n_clicks=0
        )
    ]
)

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            dbc.Col([
                dbc.Container([
                    dbc.Row([
                            html.H3(children='OPTION PRICING - BLACK-SCHOLES MODEL',
                                style={'text-align': 'center'}
                                ),
                        html.P(
                            'The Black-Scholes model, developed by economists Fischer Black, Myron Scholes, and '
                            'Robert Merton in the early 1970s, is a fundamental framework for valuing financial options.'
                            ' This model revolutionized the field of finance by providing a mathematical formula to '
                            'estimate the fair market price of European-style options. It takes into account factors '
                            'such as the current stock price, strike price, time to maturity, volatility of the '
                            'underlying asset, and the risk-free interest rate to calculate the options theoretical '
                            'value. The Black-Scholes model has become a cornerstone of modern finance, enabling '
                            'investors and financial institutions to make informed decisions about options trading, '
                            'risk management, and portfolio optimization.'
                            , style={'textAlign': 'left'}),
                    ], style={'align': 'center'}),  # , className='border'),

                    html.Hr(),
                    # inputs
                    dbc.Row([
                        dbc.Col([
                            spot_price,
                        ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),
                        dbc.Col([
                            strike_price,
                        ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),
                        dbc.Col([
                           maturity,
                        ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),

                        dbc.Col([
                            volatility,
                        ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),
                        dbc.Col([
                            interest_rate,
                        ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),

                        dbc.Col([
                            cal_button,
                        ], xs=2, sm=2, md=2, lg=2, xl=2, className='p-3'),

                        html.Hr(),
                        html.Br(),

                        html.Div(id="output", style={'width':'100%', "height": "65vh"},
                                                          className="overflow-auto")
                    ],className='align-items-end', justify='center')
                ])
            ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                            className='p-3')
        ]),

    ], fluid=True, class_name='g-0 vh-100', ) #,


# Define a callback to calculate the option price
@callback(
    Output("output", "children"),
    Input("calculate-button", "n_clicks"),
    Input("spot-price", "value"),
    Input("strike-price", "value"),
    Input("time-to-maturity", "value"),
    Input("sigma", "value"),
    Input("interest-rate", "value"),
)

def calculate_option_price(n_clicks, spot_price, strike_price, time_to_maturity, volatility, interest_rate):
    if "calculate-button" == ctx.triggered_id:
        #print('BUTTON TRIGGERED')
        data_call = BS(float(spot_price), float(strike_price), float(interest_rate), float(volatility), float(time_to_maturity), 'C')
        data_put = BS(float(spot_price), float(strike_price), float(interest_rate), float(volatility), float(time_to_maturity), 'P')
        df = pd.DataFrame()
        df['Metric'] = ['Option price', 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho']
        df['Call'] = data_call
        df['Put'] = data_put
        df = df.round(2)
        #print(df.round(2))
        table = dash_table.DataTable(
            df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
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
        )

        return [html.H2('Option Metrics'), table]


# if __name__ == "__main__":
#     app.run_server()
