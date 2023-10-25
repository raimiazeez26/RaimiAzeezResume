from datetime import date
import dash
from dash import Dash, html, dcc, ctx, dash_table, callback
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import dash_loading_spinners as dls
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from .side_bar import sidebar
from .armotization_schedule import run_armotization

dash.register_page(__name__,  order=5, name='Amortization Schedule')

#==========================================================
#input parameters 
#===========================================================

principal = html.Div([
    html.P('Loan Principal'),
    dbc.Input(id='principal', type='number', min = 1000, max = 1000000,
              value='100000')
])

interestrate = html.Div([
    html.P('Annual Interest Rate(%)'),
    dbc.Input(id='interest-rate', type='number', min = 1, max = 50,
              value='2')
])

loanyears = html.Div([
    html.P('Loan Period (Years)'),
    dbc.Input(id='loan-period', type='number', min = 1, max = 50,
              value='10')
])


run_button = html.Div(
    [
        dbc.Button(
            "Calculate", id="run-button", className="me-2", n_clicks=0
        )
    ]
)

loan_start_date = html.Div([
    html.P('Loan Start Date'),
    dcc.DatePickerSingle(
        id='loan-start-date',
        min_date_allowed=date(1990, 1, 1),
        #max_date_allowed=date(201, 9, 19),
        initial_visible_month=date.today(),
        date=date.today()
    )
])


# creates the Dash App
#app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

def layout():
    return dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2,
            #className = 'border'
            ),

            dbc.Col(
                [
                    html.H3('ARMOTIZATION SCHEDULE', style={'textAlign': 'center'}, className='p4'),
                    html.P('A simple python script which calculates Fixed rated amortization Schedule',
                           'based on input values.'

                           , style={'textAlign': 'center'}),

                    html.Hr(),

                    dbc.Container([

                        # inputs
                        dbc.Row([
                            dbc.Col([
                                principal,
                            ], xs=2, sm=2, md=2, lg=2, xl=2, className='align-items-end'),
                            dbc.Col([
                                interestrate,
                            ], xs=2, sm=2, md=2, lg=2, xl=2, className='align-content-end'),
                            dbc.Col([
                                loanyears,
                            ], xs=2, sm=2, md=2, lg=2, xl=2, className='align-self-end mr-3'),
                            dbc.Col([
                                loan_start_date,
                            ], xs=2, sm=2, md=2, lg=2, xl=2),
                            dbc.Col([
                                run_button,
                            ], xs=2, sm=2, md=2, lg=2, xl=2),

                        ],  className='align-items-end', justify='center'),

                        html.Br(),

                        dbc.Row([
                            dbc.Col([

                                dls.Hash(html.Div(
                                    # [html.H3('AMOTIZATION SCHEDULE', style={'textAlign': 'center'}),
                                    # table
                                    # ],
                                    id='arm-table'),
                                    color="#435278",
                                    speed_multiplier=2,
                                    size=50, ),

                            ], xs=10, sm=10, md=12, lg=12, xl=12, xxl=12,
                                className='p-3')
                        ])
                    ])

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3'
            )
        ]
    )
], fluid=True, class_name='g-0', # p-4
    style={"height": "99vh", 'background-size': '100%'})

@callback(
    Output('arm-table', 'children'),
    Input('principal', 'value'),
    Input('interest-rate', 'value'),
    Input('loan-period', 'value'),
    Input('loan-start-date', 'date'),
    Input('run-button', 'n_clicks'),
    prevent_initial_call=True
    
)
def arm(prin, inte, ln_yrs, ln_strt_date, n_clicks):
    # print(ln_strt_date)

    if "run-button" == ctx.triggered_id:
        #print(prin)
        #print(type(prin))

        data = run_armotization(float(prin), float(inte), float(ln_yrs), ln_strt_date)
        data['Date'] = data['Date'].astype(str)

        # create a number-based filter for columns with integer data
        col_defs = []
        for i in data.columns:
            col_defs.append({"field": i})

        table = [
            html.H5(f'{ln_yrs} years Fixed Rate amotization schedule at {inte}% Annual Interest Rate',
                    style={'textAlign': 'center'}),
            dag.AgGrid(
                id="my-table",
                rowData=data.to_dict("records"),
                columnDefs=col_defs,
                defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth": 115},
                columnSize="sizeToFit",
                # dashGridOptions={"pagination": True, "paginationPageSize":10},
                className="ag-theme-alpine",
            )]

        return table

        # else:
        return PreventUpdate

