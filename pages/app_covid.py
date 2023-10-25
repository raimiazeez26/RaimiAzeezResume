import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from .side_bar import sidebar
from .COVID19_timelapse import covid_map

dash.register_page(__name__, title='Covid-19 TimeLapse', order=4, name='Covid-19')

fig = covid_map()

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
                    html.H3('Covid-19 TimeLapse', style={'textAlign':'center'}, className='p4'),
                    html.P('Following the questions about COVID in Africa, I decided to visualize the spread of COVID-19 '
                           'around the world from Jan 2020 up to date using data from the John Hopkins data repository.'
                           'What happened in Africa? Why was the spread so limited compared to other parts of the world?'
                           , style={'textAlign': 'left'}),

                    dcc.Markdown('''
                            What happened in Africa? Why was the spread so limited compared to other parts of the world?
                            * Inaccurate/inconsistent data reporting?'
                            * Early herd Immunity?'
                            * Natural resistance to the virus?
                            ''', style={'textAlign': 'left'}),

                    dcc.Markdown('''
                       I used data from [John Hopkins repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) 
                       to visualize the growth of COVID-19 from January 2020 up till date. Raw data was collected from 
                       the repository which was processed and visualized using plotly
                       ''', style={'textAlign': 'left'}),

                    html.Hr(),
                    dcc.Graph(figure=fig, id='line_chart'),

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,
                className='p-3'
            )
        ]
    )
])


