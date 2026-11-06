"""Structured resume page for Raimi Azeez Babatunde."""

import dash
import dash_bootstrap_components as dbc
from dash import html


dash.register_page(__name__, order=3, name="Resume")


def section(title, children):
    # Dash drops nested lists, so flatten list children into the section.
    body = children if isinstance(children, list) else [children]
    return html.Section(
        [html.H2(title, className="h4 border-bottom pb-2 mb-3"), *body],
        className="mb-4",
    )


def experience(company, role, dates, location, bullets):
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(html.H3(company, className="h5 mb-1"), md=8),
                        dbc.Col(html.P(location, className="text-muted text-md-end mb-1"), md=4),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.P(role, className="fw-semibold mb-2"), md=8),
                        dbc.Col(html.P(dates, className="text-muted text-md-end mb-2"), md=4),
                    ]
                ),
                html.Ul([html.Li(item) for item in bullets], className="mb-0"),
            ]
        ),
        className="mb-3",
    )


def project(title, description, tools, href):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(title, className="h6"),
                    html.P(description, className="small"),
                    html.P([html.Strong("Tools: "), tools], className="small text-muted"),
                    html.A("View project", href=href, target="_blank", rel="noopener noreferrer"),
                ]
            ),
            className="h-100",
        ),
        xs=12,
        md=6,
        className="mb-3",
    )


layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=dash.get_asset_url("Raimi Portrait.jpg"),
                                alt="Portrait of Raimi Azeez Babatunde",
                                className="img-fluid rounded",
                                style={
                                    "width": "100%",
                                    "maxHeight": "320px",
                                    "objectFit": "cover",
                                    "objectPosition": "center 25%",
                                },
                            ),
                            xs=12,
                            md=3,
                            className="mb-3 mb-md-0",
                        ),
                        dbc.Col(
                            [
                                html.H1("Raimi Azeez Babatunde", className="display-6 fw-bold"),
                                html.P("Data Scientist | Quantitative Developer | Financial Engineering", className="lead"),
                                html.P(
                                    "Data scientist and quantitative developer with an MSc in Financial Engineering, applying "
                                    "machine learning, statistical analysis, and NLP to business and financial problems. "
                                    "Experienced building systematic trading systems, backtesting frameworks, and production ML "
                                    "models across freelance, startup, and institutional environments, and translating analysis "
                                    "into measurable gains in efficiency, revenue, and portfolio performance."
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.A("Email", href="mailto:raimiazeez26@gmail.com"), xs=6, md="auto"),
                                        dbc.Col(html.A("Phone", href="tel:+2348025831825"), xs=6, md="auto"),
                                        dbc.Col(html.A("Website", href="https://raimiazeez26.github.io/", target="_blank", rel="noopener noreferrer"), xs=6, md="auto"),
                                        dbc.Col(html.A("LinkedIn", href="https://www.linkedin.com/in/raimi-azeez/", target="_blank", rel="noopener noreferrer"), xs=6, md="auto"),
                                        dbc.Col(html.A("GitHub", href="https://github.com/raimiazeez26", target="_blank", rel="noopener noreferrer"), xs=6, md="auto"),
                                    ],
                                    className="g-2",
                                ),
                            ],
                            xs=12,
                            md=9,
                        ),
                    ],
                    align="center",
                )
            ),
            className="mb-4 shadow-sm",
        ),
        section(
            "Professional Experience",
            [
                experience(
                    "Aquion",
                    "Co-Founder and Head of Trading Systems",
                    "January 2026 – Present",
                    "Lagos, Nigeria",
                    [
                        "Architect and build automated strategy execution systems for crypto and FX markets, turning indicator-based, ML, and correlation/basket signals into production-ready workflows.",
                        "Design and implement backtesting and optimization frameworks to evaluate and refine algorithmic trading models across asset classes and strategy types.",
                    ],
                ),
                experience(
                    "Lagos State Internal Revenue Service",
                    "Senior Revenue Supervisor",
                    "July 2024 – Present",
                    "Lagos, Nigeria",
                    [
                        "Manage accurate and timely tax remittance for 40+ companies, ensuring adherence to regional tax regulations and financial transparency.",
                        "Collate and analyze tax collection reports from 7 tax stations in the region, synthesizing key data into insights reported directly to the director's office.",
                    ],
                ),
                experience(
                    "Upwork",
                    "Data Scientist and Quantitative Developer (Freelance)",
                    "December 2023 – Present",
                    "Remote",
                    [
                        "Deliver freelance engagements in quantitative finance, data science, machine learning, and AI for clients across industries.",
                        "Maintain Top Rated Freelancer status, reflecting consistently high client satisfaction and quality of work.",
                    ],
                ),
                experience(
                    "Xavier McAllister Capital",
                    "Data Scientist",
                    "December 2021 – November 2023",
                    "Lagos, Nigeria",
                    [
                        "Developed and deployed a customer-facing LLM chatbot, boosting customer engagement by 30% and profit by 20%.",
                        "Analyzed historical trade results and market data in Python to identify correlation patterns across strategy types and optimal trading windows, contributing to a 20% improvement in portfolio returns.",
                        "Coordinated data analytics projects, aligning objectives with business goals and achieving a 20% increase in overall efficiency.",
                        "Collaborated cross-functionally to analyze large datasets, uncovering market trends that led to a 20% increase in market share.",
                    ],
                ),
                experience(
                    "Xavier McAllister Capital",
                    "Financial & Investment Data Analyst",
                    "September 2021 – December 2021",
                    "Lagos, Nigeria",
                    [
                        "Executed daily trades, contributing to a 10% increase in investment returns.",
                        "Developed risk assessment algorithms that reduced potential losses by 18%.",
                        "Processed extensive datasets, streamlining project timelines by 15%.",
                        "Produced and presented monthly trade reports, improving team transparency and stakeholder communication.",
                    ],
                ),
                experience(
                    "Hamoye",
                    "Data Science Intern",
                    "March 2021 – July 2021",
                    "Remote",
                    [
                        "Built machine learning models for image recognition and time-series prediction.",
                        "Identified machine learning solutions to real-world problems through structured case study analysis.",
                        "Conducted exploratory data analysis and visualization to support model preparation and feature engineering.",
                    ],
                ),
                experience(
                    "Daydream Pictures",
                    "Business Development Executive",
                    "September 2014 – September 2021",
                    "Lagos, Nigeria",
                    [
                        "Developed plans for revenue and client-base growth and maintained long-term client relationships.",
                        "Managed social media channels that grew to more than 13,000 followers across platforms.",
                    ],
                ),
            ],
        ),
        section(
            "Education",
            [
                dbc.Row(
                    [
                        dbc.Col(html.Strong("WorldQuant University"), md=4),
                        dbc.Col(
                            [
                                "MSc, Financial Engineering",
                                html.Div(
                                    "Coursework: Quantitative Finance, Portfolio and Risk Management, Machine Learning and AI, Algorithmic Trading Strategies",
                                    className="small text-muted",
                                ),
                            ],
                            md=5,
                        ),
                        dbc.Col("January 2023 – December 2024", md=3, className="text-md-end text-muted"),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Strong("Ustacky"), md=4),
                        dbc.Col("Data Science MicroDegree", md=5),
                        dbc.Col("March 2021 – June 2021", md=3, className="text-md-end text-muted"),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Strong("Lagos State University, Ojo"), md=4),
                        dbc.Col("BSc, Fisheries | CGPA 4.37/5.00", md=5),
                        dbc.Col("2011 – January 2016", md=3, className="text-md-end text-muted"),
                    ]
                ),
            ],
        ),
        section(
            "Core Skills",
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Quantitative & Data Science", className="h6"),
                            html.P("Python, machine learning, NLP, statistical analysis, time-series analysis, algorithmic trading, backtesting and strategy optimization, web scraping"),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.H3("Analytics & Engineering", className="h6"),
                            html.P("SQL and DBMS, data exploration, API integration, data visualization, Tableau, Power BI, Excel, AWS, Azure Data Studio"),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.H3("Finance & Leadership", className="h6"),
                            html.P("Quantitative finance, financial modeling, risk assessment, investment analysis, valuation, business strategy, strategic planning, cross-functional collaboration"),
                        ],
                        md=4,
                    ),
                ],
                className="g-3",
            ),
        ),
        section(
            "Selected Projects",
            dbc.Row(
                [
                    project(
                        "Automated Client Onboarding",
                        "An n8n workflow that captures client requirements, validates intake, and coordinates onboarding records and tasks.",
                        "n8n, Python, Google Sheets, Google Drive, Gmail",
                        "https://github.com/raimiazeez26/n8n-client-onboarding",
                    ),
                    project(
                        "Job Application Tracker Automation",
                        "n8n workflows for recording applications, requesting job-to-CV matching, and updating application status.",
                        "n8n, AI matching, Google Sheets",
                        "https://github.com/raimiazeez26/n8n-job-application-tracker",
                    ),
                    project(
                        "Interactive Resume & Analytics",
                        "A multi-page app with financial engineering, forecasting, volatility, clustering, and dashboard demonstrations.",
                        "Python, Dash, pandas, Plotly, scikit-learn",
                        "https://github.com/raimiazeez26/RaimiAzeezResume",
                    ),
                    project(
                        "MT5pyTrader",
                        "A Python module for connecting algorithmic trading scripts with MetaTrader 5.",
                        "Python, MetaTrader 5",
                        "https://github.com/raimiazeez26/MT5pytrader",
                    ),
                ],
                className="g-3",
            ),
        ),
        section(
            "Professional Certifications",
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        [html.Strong("Senior Chartered Public Manager (SCPM)"), " — Chartered Institute of Public Management of Nigeria (CIPMN)"]
                    ),
                    dbc.ListGroupItem(
                        [html.Strong("Business Intelligence & Data Analyst (BIDA)"), " — Corporate Finance Institute (2023)"]
                    ),
                    dbc.ListGroupItem(
                        [html.Strong("Financial Modeling & Valuation Analyst (FMVA)"), " — Corporate Finance Institute (2022)"]
                    ),
                    dbc.ListGroupItem(
                        [html.Strong("Machine Learning for Finance"), " — Udemy (2022)"]
                    ),
                    dbc.ListGroupItem(
                        [html.Strong("AWS Machine Learning Foundations"), " — Udacity (2022)"]
                    ),
                ],
                flush=True,
            ),
        ),
    ],
    fluid=True,
    className="py-4",
)
