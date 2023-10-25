#import
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, order=3)

#interest buttons
interests_buttons = html.Div(
    [
        dbc.Button("Finance", outline=True, color="primary", className="me-1"),
        dbc.Button("Analytics", outline=True, color="primary", className="me-1"),
        dbc.Button("Business", outline=True, color="primary", className="me-1"),
        dbc.Button("Technology", outline=True, color="primary", className="me-1"),
        dbc.Button("Algorithmic Trading", outline=True, color="primary", className="me-1"),
        ]
)

# resume sample template from https://zety.com/
layout = html.Div([
    dbc.Row([

        #Biodata
       # dbc.Col([
        dcc.Markdown('# Raimi Azeez Babatunde', style={'textAlign':'center'}),
        dcc.Markdown('#### Data Scientist', style={'textAlign':'center'}),
        html.Hr(),

        dbc.Row([
            dbc.Col([
                dbc.Col([
                    html.I(className="fa-solid fa-envelope"),  # <i class="fa-solid fa-envelope"></i>
                    dcc.Markdown('###### &ensp; raimiazeez26@gmail.com',
                                 style={'textAlign': 'center'}),
                ], width={"size": 3}, className='d-inline-flex'),

                dbc.Col([
                    html.I(className="fa-solid fa-phone"),  # <i class="fa-solid fa-envelope"></i>
                    dcc.Markdown('###### &ensp; +2348025831825',
                                 style={'textAlign': 'center'}),
                ], width={"size": 3}, className='d-inline-flex'),
                dbc.Col([
                    html.I(className="fa-regular fa-globe-pointer p-1"),  # <i class="fa-brands fa-kaggle"></i>
                    html.A('Website  ', href='https://raimiazeez26.github.io/', target="_blank",
                           style={'textAlign': 'center'})
                ], width={"size": 3}, className=' d-inline-flex', style={'textAlign': 'center'}),
            ], width='9', style={'align': 'right'})
        ], justify="center", className='pt-1 pb-1'),

        # social media
        dbc.Row([
            dbc.Col([
                dbc.Col([
                    html.I(className="fa-brands fa-github p-1"),  # <i class="fa-brands fa-github"></i>
                    html.A('GitHub  ', href='https://github.com/raimiazeez26', target="_blank",
                           style={'textAlign': 'center'})
                ], width={"size": 2}, className='d-inline-flex'),

                dbc.Col([
                    html.I(className="fa-brands fa-linkedin p-1"),
                    html.A('LinkedIn  ', href='https://www.linkedin.com/in/raimi-azeez/', target="_blank",
                           style={'textAlign': 'left'})
                ], width={"size": 2}, className='d-inline-flex'),

                dbc.Col([
                    html.I(className="fa-brands fa-medium p-1"),
                    html.A('Medium  ', href='https://medium.com/@raimiazeez26', target="_blank",
                           style={'textAlign': 'left'})
                ], width={"size": 2}, className='d-inline-flex'),

                dbc.Col([
                    html.I(className="fa-brands fa-kaggle p-1"),  # <i class="fa-brands fa-kaggle"></i>
                    html.A('Kaggle  ', href='https://www.kaggle.com/raimiazeezbabatunde', target="_blank",
                           style={'textAlign': 'left'})
                ], width={"size": 2}, className='d-inline-flex'),
            ], width='9', style={'align': 'center'})
        ], justify="center", style={'align': 'center'}),

        # ], width={"size": 8}, className= 'flex-column p-3'), #, "offset": 4
    ], justify="center", style={'align': 'center'}),

    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(" I am a Data Scientist with vast and efficient knowledge in using "
                   "python, data analysis, visualization,  and machine learning models & techniques to deliver "
                   "insights and implement action-oriented solutions to business problems. My goal is to work in "
                   "an environment where my potential and capabilities will be developed and utilized to attain "
                   " the organization's goals and make a real-life impact.",
                   # ' \n',
                   style={'textAlign': 'left', 'white-space': 'pre-wrap'},
                   # className='flex-column'
                   ),
            ], width={"size": 9, "offset": 1}, className='flex-column',
                style={'textAlign': 'center'}),

    ], justify="center", style={'align': 'center'}),

    #Skills
    html.Hr(),
    dcc.Markdown('### Core Competencies', style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
        * Python Programming
        * Machine Learning
        * Natural Language Processing (NLP)
        * Web Scraping
        * Statistical Analysis
        ''')
        ], width={"size": 3, "offset": 1},
            style={'textAlign': 'left'}),
        dbc.Col([
            dcc.Markdown('''
        * Time Series Analysis
        * Data Exploration & Analysis
        * Data Visualization
        * Microsoft PowerBI & Excel
        * [Tableau](https://public.tableau.com/app/profile/raimi.azeez.babatunde)
        ''')
        ], width=3, style={'textAlign': 'left'}),
        dbc.Col([
            dcc.Markdown('''
        * API Integration
        * SQL & DBMS
        * AWS & Azure Data Studio
        * Leadership
        * Business Strategy
        ''')
        ], width=3, style={'textAlign': 'left'})
    ], justify='center'),


    # #Work History
    html.Hr(),
    dcc.Markdown('### Professional Experience', style={'textAlign': 'center'}),
    html.Hr(),
    #Experience 1
    dbc.Row([
        #company, location
        dbc.Row([
            dbc.Col([
                dcc.Markdown('#### Xavier Mcallister Capital',
                             style={'textAlign': 'left'}),
            ],width = '4'),

            dbc.Col([
                dcc.Markdown('###### Lagos, Nigeria',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify = 'center'),

        # Job Title, Date
        dbc.Row([
            dbc.Col([
                dcc.Markdown('##### Data Scientist',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Dec. 2021 - Present',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),


        # Responsibilities
        dbc.Row([
            dbc.Col([
                html.Ul([
                    html.Li(
                            'Developed and deployed a cutting-edge chatbot using Large Language Models (LLM) technology, resulting '
                            'in a 30% increase in customer engagement and a 20% increase in profit.'),
                    html.Li('Coordinated the execution of data analytics projects, aligning objectives with business goals, resulting in a '
                            '20% increase in overall efficiency'),
                    html.Li('Analyzed historical and technical indicator data using Python programming to identify profitable trading '
                            'opportunities, resulting in an increase of 20% in overall portfolio returns.'),
                    html.Li('Collaborated with cross-functional teams to gather and analyze large datasets, identifying key trends and '
                            'patterns that informed strategic business decisions, resulting in a 20% increase in market share.'),
                    html.Li('Actively pursued professional development, earning certifications in areas such as '
                            'Business Intelligence & Data Analytics and Machine Learning..'),
                ], style={'textAlign': 'left'})
            ], width='8')
        ], justify='center'),
    ]),
    html.Br(),

    # Experience 2
    dbc.Row([
        # company, location
        dbc.Row([
            dbc.Col([
                dcc.Markdown('#### Xavier Mcallister Capital',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Lagos, Nigeria',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),

        # Job Title, Date
        dbc.Row([
            dbc.Col([
                dcc.Markdown('##### Financial & Investment Data Analyst',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Sept. 2021 - Dec. 2021',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),

        # Responsibilities
        dbc.Row([
            dbc.Col([
                html.Ul([
                    html.Li(
                        'Executed daily trades, yielding a profitable trading portfolio and contributing to a 10% increase in '
                            'investment returns.'),
                    html.Li('Assisted in developing algorithms for risk assessment, minimizing potential losses by 18% through '
                            'improved risk management.'),
                    html.Li('Extracted, cleaned, and processed extensive datasets from diverse sources, including user interactions '
                            'and financial transactions reducing project timelines and analysis by 15%.'),
                    html.Li('Generated and presented monthly trade activity reports, enhancing transparency and communication '
                            'within the team and with stakeholders.'),
                ], style={'textAlign': 'left'})
            ], width='8'),
        ], justify='center'),

    ]),
    html.Br(),

    #Experience 3
    dbc.Row([
        #company, location
        dbc.Row([
            dbc.Col([
                dcc.Markdown('#### Hamoye',
                             style={'textAlign': 'left'}),
            ], width = '4'),

            dbc.Col([
                dcc.Markdown('###### Remote',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify = 'center'),

        # Job Title, Date
        dbc.Row([
            dbc.Col([
                dcc.Markdown('##### Data Science Intern',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Sept. 2021 - Nov. 2021',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),


        # Responsibilities
        dbc.Row([
            dbc.Col([
                html.Ul([
                    html.Li(
                        'Successfully developed machine learning models such as image recognition & time series prediction models.'),
                    html.Li('Worked with cross-functional teams on different case studies, identifying machine learning solutions to real-world problems.'),
                    html.Li('Performed exploratory data analysis and visualization to prepare data for modelling.'),
                ], style={'textAlign': 'left'})
            ], width='8')

            ], justify='center'),

    ]),
    html.Br(),

    #Experience 4
    dbc.Row([
            #company, location
            dbc.Row([
                dbc.Col([
                    dcc.Markdown('#### Daydream Pictures',
                                 style={'textAlign': 'left'}),
                ], width = '4'),

                dbc.Col([
                    dcc.Markdown('###### Lagos, Nigeria',
                                 style={'textAlign': 'right'})
                ], width='4'),
            ], justify = 'center'),

            # Job Title, Date
            dbc.Row([
                dbc.Col([
                    dcc.Markdown('##### Business Development Executive',
                                 style={'textAlign': 'left'}),
                ], width='4'),

                dbc.Col([
                    dcc.Markdown('###### Sept. 2014 - Sept. 2021',
                                 style={'textAlign': 'right'})
                ], width='4'),
            ], justify='center'),


            # Responsibilities
            dbc.Row([
                dbc.Col([
                    html.Ul([
                        html.Li(
                            'Set goals and plans for business revenue and client base growth.'),
                        html.Li('Maintained client relationship and ensure up to retention up to 10years'),
                        html.Li('Managed its social media from to over 13k+ followers on multiple social media accounts.'),
                    ], style={'textAlign': 'left'})
                ], width='8')

                ], justify='center'),

        ]),
    html.Br(),

    #Education
    html.Hr(),
    dcc.Markdown('### Education', style={'textAlign': 'center'}),
    html.Hr(),

    # Education 1
    dbc.Row([
        # University
        dbc.Row([
            dbc.Col([
                dcc.Markdown('#### WorldQuant University',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Louisiana, USA',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),

        # Course
        dbc.Row([
            dbc.Col([
                dcc.Markdown('###### MSc Financial Engineering',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Jan. 2023 - Present',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),

    ]),
    html.Br(),

    # Education 2
    dbc.Row([
        # University
        dbc.Row([
            dbc.Col([
                dcc.Markdown('#### Ustacky',
                             style={'textAlign': 'left'}),

            ], width='8'),

        ], justify='center'),

        # Course
        dbc.Row([
            dbc.Col([
                dcc.Markdown('###### Data Science MicroDegree',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Mar. 2021 - Jun. 2021',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),

    ]),
    html.Br(),

    # Education 3
    dbc.Row([
        # University
        dbc.Row([
            dbc.Col([
                dcc.Markdown('#### Lagos State University',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Ojo Lagos, Nigeria',
                             style={'textAlign': 'right'})

            ], width='4'),

        ], justify='center'),

        # Course
        dbc.Row([
            dbc.Col([
                dcc.Markdown('###### Fisheries',
                             style={'textAlign': 'left'}),
            ], width='4'),

            dbc.Col([
                dcc.Markdown('###### Apr. 2011 - Jan. 2016',
                             style={'textAlign': 'right'})
            ], width='4'),
        ], justify='center'),

        # Responsibilities
        dbc.Row([
            dbc.Col([
                html.Ul([
                    html.Li(
                        'CGPA 4.37/5.00'),
                ], style={'textAlign': 'left'})
            ], width='8')
        ], justify='center'),

    ]),
    html.Br(),

    # Certifications
    html.Hr(),
    dcc.Markdown('### Certifications', style={'textAlign': 'center'}),
    html.Hr(),
    #Certification 1
    dbc.Row([
        dbc.Col([
            dcc.Markdown('2023',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('###### Business Intelligence & Data Analyst (BIDA)\n',
                         #'San Francisco State University - San Francisco, CA',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5),
        dbc.Col([
            dcc.Markdown('Corporate Finance Institute (CFI)',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=3)
    ], justify='center'),

    # Certification 2
    dbc.Row([
        dbc.Col([
            dcc.Markdown('2022',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('###### Financial Modeling & Valuation Analyst (FMVA)\n',
                         # 'San Francisco State University - San Francisco, CA',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5),
        dbc.Col([
            dcc.Markdown('Corporate Finance Institute (CFI)',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=3)
    ], justify='center'),

    # Certification 3
    dbc.Row([
        dbc.Col([
            dcc.Markdown('2022',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('###### Machine Learning for Finance (2022)\n',
                         # 'San Francisco State University - San Francisco, CA',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5),
        dbc.Col([
            dcc.Markdown('Udemy',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=3)
    ], justify='center'),

    # Certification 4
    dbc.Row([
        dbc.Col([
            dcc.Markdown('2022',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('###### AWS Machine Learning Foundation\n',
                         # 'San Francisco State University - San Francisco, CA',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5),
        dbc.Col([
            dcc.Markdown('Udacity',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=3)
    ], justify='center'),

    # Interests
    html.Hr(),
    dcc.Markdown('### Interests', style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        interests_buttons,
    ], justify='center', className='pt-3'),

    # Community
    html.Hr(),
    dcc.Markdown('### Community', style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dcc.Markdown('###### [TheRoom](https://www.theroom.com/) - Member',
                     style={'white-space': 'pre'},
                     className='ms-3'),
    ], justify='center', className='pt-3'),

])
