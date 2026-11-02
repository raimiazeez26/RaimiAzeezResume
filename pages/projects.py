"""Selected portfolio work and links to interactive demonstrations."""

import dash
import dash_bootstrap_components as dbc
from dash import html

from .side_bar import sidebar

dash.register_page(__name__, order=0, name="Projects")


def project_card(title, description, technology, links):
    """Build a consistent project card from its summary and links."""
    actions = [
        html.A(label, href=url, target="_blank", rel="noopener noreferrer", className="me-3")
        for label, url in links
    ]
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.P(description, className="card-text"),
                html.P([html.Strong("Tools: "), technology], className="small text-muted"),
                html.Div(actions),
            ]
        ),
        className="h-100 shadow-sm",
    )


def layout():
    projects = [
        (
            "Automated Client Onboarding",
            "An n8n onboarding workflow that validates client intake, creates a structured client record and workspace, prepares onboarding tasks, and sends notifications. This app includes an external intake form for the main workflow.",
            "n8n, Python, Google Sheets, Google Drive, Gmail, Dash",
            [
                ("Open onboarding form", "/n8n-client-onboarding"),
                ("Job application", "/n8n-job-application"),
                ("AI job match", "/n8n-job-match"),
                ("Update application status", "/n8n-application-status"),
                ("Workflow source", "https://github.com/raimiazeez26/n8n-client-onboarding"),
            ],
        ),
        (
            "Interactive Resume & Analytics",
            "A multi-page Dash application with financial engineering, data science, and analytics demonstrations, including ARIMA, GARCH, option pricing, clustering, and dashboards.",
            "Python, Dash, pandas, Plotly, scikit-learn",
            [
                ("Live app", "https://raimi-azeez-bb3c8dbeda1f.herokuapp.com/projects"),
                ("Source code", "https://github.com/raimiazeez26/RaimiAzeezResume"),
            ],
        ),
        (
            "Personal Portfolio Website",
            "A static portfolio presenting selected projects, professional background, skills, and contact information.",
            "HTML, CSS/SCSS, JavaScript, GitHub Pages",
            [
                ("Live website", "https://raimiazeez26.github.io/"),
                ("Source code", "https://github.com/raimiazeez26/raimiazeez26.github.io"),
            ],
        ),
        (
            "MT5pyTrader",
            "A Python module for connecting algorithmic trading scripts with MetaTrader 5.",
            "Python, MetaTrader 5",
            [
                ("Source code", "https://github.com/raimiazeez26/MT5pytrader"),
                ("Strategy article", "https://medium.com/insiderfinance/creating-a-simple-ema-cross-strategy-trading-script-using-mt5pytrader-c1f9e1b6a17b"),
            ],
        ),
    ]

    project_columns = [
        dbc.Col(
            project_card(title, description, technology, links),
            xs=12,
            md=6,
            className="mb-4",
        )
        for title, description, technology, links in projects
    ]

    demo_pages = [
        ("ARIMA Forecasting", "/app-arima"),
        ("GARCH Volatility", "/app-garch"),
        ("Black–Scholes Option Pricing", "/app-blackscholes"),
        ("K-Means Clustering", "/app-clustering"),
        ("Northwind Dashboard", "/app-northwind"),
        ("COVID-19 Timeline", "/app-covid"),
    ]

    return html.Div(
        dbc.Row(
            [
                dbc.Col(sidebar(), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col(
                    [
                        html.H2(
                            "Selected Projects",
                            className="text-center mb-3",
                        ),
                        html.P(
                            "A selection of interactive applications, reusable tools, and portfolio work. "
                            "Each project links to its live version or source.",
                            className="mb-4",
                        ),
                        dbc.Row(project_columns),
                        html.Hr(),
                        html.H3("Interactive demos in this app", className="mb-3"),
                        dbc.ListGroup(
                            [
                            dbc.ListGroupItem(label, href=href, action=True)
                                for label, href in demo_pages
                            ],
                            className="mb-4",
                        ),
                        html.Hr(),
                        html.H4("More work"),
                        html.P(
                            [
                                html.A(
                                    "GitHub",
                                    href="https://github.com/raimiazeez26",
                                    target="_blank",
                                    rel="noopener noreferrer",
                                    className="me-3",
                                ),
                                html.A(
                                    "Tableau",
                                    href="https://public.tableau.com/app/profile/raimi.azeez.babatunde",
                                    target="_blank",
                                    rel="noopener noreferrer",
                                    className="me-3",
                                ),
                                html.A(
                                    "Kaggle",
                                    href="https://www.kaggle.com/raimiazeezbabatunde",
                                    target="_blank",
                                    rel="noopener noreferrer",
                                ),
                            ]
                        ),
                    ],
                    xs=8,
                    sm=8,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                    className="p-3",
                ),
            ]
        )
    )
