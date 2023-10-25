import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from .side_bar import sidebar

dash.register_page(__name__, order=0)

def layout():
    return html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.H2('Welcome to my Project Page', style={'textAlign':'center'}, className='p4'),
                    html.H5('This Page is Actively Updated', style={'textAlign': 'center'}, className='p4 text-warning'),
                    html.P('This Project App was created using Dash. All projects contained within this project app '
                           'was completed using python. Feel free to check my github for source codes or send an email '
                           'to request. '
                           
                           'Please switch Theme (top right corner) for varying experience for each app!'
                           , style={'textAlign': 'left'}),

                    dcc.Markdown('''
                            Other Project Sources
                            * [Github](https://github.com/raimiazeez26)
                            * [Tableau](https://public.tableau.com/app/profile/raimi.azeez.babatunde)
                            * [Kaggle](https://www.kaggle.com/raimiazeezbabatunde)
                            ''', style={'textAlign': 'left'}),

                    html.Hr(),
                    #dcc.Graph(figure=fig, id='line_chart'),

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3'
            )
        ]
    )
])


