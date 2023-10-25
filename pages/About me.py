import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', order=0)

green_text = {'color':'green'}
#image card
picture_card = dbc.Card(
    [
        dbc.CardImg(src="assets/portrait.jpeg", top=True),
        #dbc.CardBody(
            #html.P("This card has an image at the top", className="card-text")
        #),
    ],
    #style={"width": "21rem"},
    className='border rounded-lg',
)

def layout():
    return dbc.Row([
        # put image here
        dbc.Col([
            picture_card
        ], xs=1, sm=2, md=2, lg=3, xl=3, xxl=3, #style={'align': 'center'},
            className='pt-5'), #width={"size": 3} #float-right

        dbc.Col([
            html.H1('Raimi Azeez Babatunde', style={'textAlign': 'center'}, className='p4'),
            html.Hr(),
            #picture_card,
            html.P("Hi, I'm glad you found me.\n \n"
                 "Welcome to my world of data-driven wonders! I'm Azeez, your go-to wizard for turning raw data "
                 "into game-changing insights. With a passion for Python, data analysis, visualization, "
                 "and machine learning, I'm on a mission to unravel the untold stories hidden in data.",
                 style={'textAlign': 'left'}),

            html.P("From crunching numbers to crafting visually stunning dashboards, I thrive on transforming "
                 "complexity into clarity. My insatiable curiosity and love for problem-solving keep me at "
                 "the forefront of cutting-edge technologies and trends",
                   style={'textAlign': 'left'}),

            html.P("When I'm not geeking out on data, you can find me exploring the fascinating realms of "
                 "Finance, or in the field flexing my photography skills.\n"
                 "Ready to embark on a data-driven adventure? Let's innovate together!",
                   style={'textAlign': 'left'}),

            html.P("With my diverse skill set, I am suitable and well-equipped to excel in a variety of roles:\n",
                   style={'textAlign': 'left'}),

            dcc.Markdown('''
                * Data Scientist
                * Quantitative Analyst (Quant)
                * Financial Analyst (with Data Emphasis)
                * Data Analyst
                * Data Engineer
                * Business Intelligence Analyst
                * Machine Learning Engineer
                * Natural Language Processing (NLP) Specialist
                * Data Visualization Specialist
                * Technical Lead / Manager
                * Research Scientist (NLP)
                * Business Strategy Analyst
                * Data Operations Manager
            ''', style={'textAlign': 'left'})
        ], xs=6, sm=6, md=8, lg=8, xl=8, xxl=8, className='align-content-around flex-wrap') #width={'size':6}

], justify='center', className='p-3')