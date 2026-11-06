"""Portfolio project index with internal detail pages and source links."""

import dash
import dash_bootstrap_components as dbc
from dash import html

from .side_bar import sidebar

dash.register_page(__name__, order=0, name="Projects")


PROJECTS = [
    {
        "title": "Automated Client Onboarding",
        "description": "An n8n onboarding workflow that validates client intake, creates a structured client record and workspace, prepares onboarding tasks, and sends notifications.",
        "technology": "n8n, Python, Google Sheets, Google Drive, Gmail, Dash",
        "kind": "AI & Automation",
        "page": "/n8n-client-onboarding",
        "repository": "https://github.com/raimiazeez26/n8n-client-onboarding",
    },
    {
        "title": "Interactive Resume & Analytics",
        "description": "A multi-page Dash application with data science, analytics, and financial engineering demonstrations.",
        "technology": "Python, Dash, pandas, Plotly, scikit-learn",
        "kind": "Portfolio",
        "page": "https://raimi-azeez-bb3c8dbeda1f.herokuapp.com/projects",
        "repository": "https://github.com/raimiazeez26/RaimiAzeezResume",
    },
    {
        "title": "Personal Portfolio Website",
        "description": "A static portfolio presenting selected projects, professional background, skills, and contact information.",
        "technology": "HTML, CSS/SCSS, JavaScript, GitHub Pages",
        "kind": "Portfolio",
        "page": "https://raimiazeez26.github.io/",
        "repository": "https://github.com/raimiazeez26/raimiazeez26.github.io",
    },
    {
        "title": "Backtest Dashboard",
        "description": "An interactive foreign-exchange strategy backtesting dashboard. Configure indicator-based entry and exit rules, review historical results, and inspect trading performance metrics.",
        "technology": "Python, Dash, pandas, Plotly, technical indicators, TradingView data",
        "kind": "Quant & Financial Engineering",
        "page": "/app-backtest",
        "repository": "https://github.com/raimiazeez26/BacktestDashboard",
    },
    {
        "title": "Content Forge",
        "description": "A Python rendering service that turns prepared social media copy into branded vertical posters and short silent videos, with HTTP endpoints designed for workflow automation.",
        "technology": "Python, Pillow, FastAPI, FFmpeg, Docker, n8n",
        "kind": "AI & Automation",
        "page": "/project/content-forge",
        "repository": "https://github.com/raimiazeez26/content-forge",
    },
    {
        "title": "AI Financial Analyst Workflow",
        "description": "A multi-stage financial research workflow that collects market data and evidence, produces structured analysis, checks claims, generates reports, and records an audit trail.",
        "technology": "n8n, OpenAI, Python, yfinance, PostgreSQL, Telegram",
        "kind": "AI & Automation",
        "page": "/project/ai-financial-analyst",
        "repository": "https://github.com/raimiazeez26/ai-financial-analyst",
    },
    {
        "title": "NGX Market Intelligence",
        "description": "A Nigerian equities analysis workspace combining a FastAPI backend with a React dashboard for stock details, technical indicators, screening, charts, and portfolio exploration.",
        "technology": "Python, FastAPI, React, TypeScript, pandas, TradingView data",
        "kind": "Quant & Financial Engineering",
        "page": "/project/ngx-market-intelligence",
        "repository": "https://github.com/raimiazeez26/NGX-Market-Inteligence",
        "private": True,
    },
    {
        "title": "BudgetMe",
        "description": "A personal budgeting web application with authenticated user flows, monthly budget management, category summaries, charts, and a yearly overview.",
        "technology": "React, TypeScript, Vite, Supabase, Recharts, Tailwind CSS",
        "kind": "Data Science & Analytics",
        "page": "/project/budgetme",
        "repository": "https://github.com/raimiazeez26/BudgetMe",
        "private": True,
    },
    {
        "title": "Boardroom AI v2",
        "description": "An evidence-grounded AI assistant that answers questions from approved company documents, verifies each claim against retrieved sources, and escalates uncertain requests for human review.",
        "technology": "n8n, PostgreSQL, pgvector, Google Drive, LLMs, Telegram",
        "kind": "AI & Automation",
        "page": "/project/boardroom-ai",
        "repository": "https://github.com/raimiazeez26/boardroom-ai-v2",
    },
    {
        "title": "RAI Automations",
        "description": "An AI revenue engine for an automation agency: prospect discovery, cited research, owner-approved outreach drafts, and a sales workspace on a PostgreSQL and pgvector memory layer.",
        "technology": "Node.js, PostgreSQL, pgvector, n8n, OpenAI, Google OAuth, Heroku",
        "kind": "AI & Automation",
        "page": "/project/rai-automations",
        "repository": "https://github.com/raimiazeez26/RAI",
        "private": True,
    },
    {
        "title": "NGX Short-Horizon Alpha",
        "description": "Reproducible research testing whether technical, point-in-time fundamental, and macro information improve cross-sectional stock selection on the Nigerian Exchange.",
        "technology": "Python, scikit-learn, pandas, walk-forward validation, bootstrap inference",
        "kind": "Quant & Financial Engineering",
        "page": "/project/ngx-short-horizon-alpha",
        "repository": "https://github.com/raimiazeez26/short_horizon_alpha_ngx",
        "private": True,
    },
    {
        "title": "ScalpAgent",
        "description": "A short-horizon scalping runtime with a browser dashboard, multi-broker adapters, cost-aware risk controls, managed exits, deterministic replay, and parallel parameter optimization.",
        "technology": "Python, FastAPI, SQLite, MT5, OANDA, Hyperliquid, JavaScript",
        "kind": "Quant & Financial Engineering",
        "page": "/project/scalpagent",
        "repository": "https://github.com/raimiazeez26/ScalpAgent",
        "private": True,
    },
    {
        "title": "EMA Crossover + VWAP Trading System",
        "description": "A multi-timeframe EMA and VWAP strategy with an MT5 backtesting and optimization pipeline and an OANDA live trading bot with Telegram alerts and end-of-day reporting.",
        "technology": "Python, MetaTrader 5, OANDA v20, TA-Lib, Telegram, Dash",
        "kind": "Quant & Financial Engineering",
        "page": "/project/ema-vwap-trading-system",
        "repository": "https://github.com/raimiazeez26/EMA_Crossover_VWAP_Strategy-v2",
    },
    {
        "title": "Northwind Sales Dashboard",
        "description": "A top-level KPI dashboard for the Maven Northwind Challenge covering revenue, orders, customers, employees, products, and order locations.",
        "technology": "Python, Dash, Plotly, pandas",
        "kind": "Data Science & Analytics",
        "page": "/app-northwind",
        "repository": "https://github.com/raimiazeez26/NorthWind-Dashboard",
    },
    {
        "title": "MT5pyTrader",
        "description": "A Python module for connecting algorithmic trading scripts with MetaTrader 5.",
        "technology": "Python, MetaTrader 5",
        "kind": "Quant & Financial Engineering",
        "page": None,
        "repository": "https://github.com/raimiazeez26/MT5pytrader",
    },
    {
        "title": "AI Financial Analyst App",
        "description": "An embedded conversational assistant for technical financial-market analysis from the original portfolio application.",
        "technology": "Dash, embedded AI analyst service",
        "kind": "AI & Automation",
        "page": "/app-aianalyist",
        "repository": "https://github.com/raimiazeez26/RaimiAzeezResume",
    },
    {
        "title": "RAIMI-ANALYST",
        "description": "An embedded technical-analysis assistant for exploring financial markets.",
        "technology": "Dash, embedded AI analyst service",
        "kind": "AI & Automation",
        "page": "/app-tagpt",
        "repository": "https://github.com/raimiazeez26/RaimiAzeezResume",
    },
    {
        "title": "Forex Trading Signals",
        "description": "Fetch technical ratings for FX pairs from TradingView and inspect the signal by timeframe.",
        "technology": "Python, Dash, TradingView TA",
        "kind": "Quant & Financial Engineering",
        "page": "/app-forexsignal",
        "repository": "https://github.com/raimiazeez26/RaimiAzeezResume",
    },
    {
        "title": "Forex Market Screener",
        "description": "Scan selected FX pairs for current technical ratings, with an optional timed refresh.",
        "technology": "Python, Dash, TradingView TA",
        "kind": "Quant & Financial Engineering",
        "page": "/app-screener",
        "repository": "https://github.com/raimiazeez26/RaimiAzeezResume",
    },
]


def project_card(project):
    """Build a consistent project card with internal and external actions."""
    actions = []
    if project.get("page"):
        actions.append(
            html.A("Project details", href=project["page"], className="btn btn-sm btn-outline-info me-2")
        )
    if project.get("private"):
        actions.append(
            html.Span(
                [html.I(className="fa-solid fa-lock me-1"), "Private repository"],
                className="badge text-bg-secondary p-2",
                title="Source available on request",
            )
        )
    else:
        actions.append(
            html.A(
                "Source code",
                href=project["repository"],
                target="_blank",
                rel="noopener noreferrer",
                className="btn btn-sm btn-outline-light",
            )
        )
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(project["kind"], className="small text-info text-uppercase fw-bold mb-2"),
                html.H4(project["title"], className="card-title"),
                html.P(project["description"], className="card-text"),
                html.P([html.Strong("Tools: "), project["technology"]], className="small text-muted"),
                html.Div(actions),
            ]
        ),
        className="h-100 shadow-sm",
    )


def layout():
    project_columns = [
        dbc.Col(project_card(project), xs=12, md=6, className="mb-4")
        for project in PROJECTS
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
                        html.H2("Selected Projects", className="text-center mb-3"),
                        html.P(
                            "Explore project overviews, interactive demonstrations, and source repositories, grouped by project type.",
                            className="mb-4",
                        ),
                        dbc.Row(project_columns),
                        html.Hr(),
                        html.H3("Interactive demos in this app", className="mb-3"),
                        dbc.ListGroup(
                            [dbc.ListGroupItem(label, href=href, action=True) for label, href in demo_pages],
                            className="mb-4",
                        ),
                        html.Hr(),
                        html.H4("More work"),
                        html.P(
                            [
                                html.A("GitHub", href="https://github.com/raimiazeez26", target="_blank", rel="noopener noreferrer", className="me-3"),
                                html.A("Tableau", href="https://public.tableau.com/app/profile/raimi.azeez.babatunde", target="_blank", rel="noopener noreferrer", className="me-3"),
                                html.A("Kaggle", href="https://www.kaggle.com/raimi.babatunde", target="_blank", rel="noopener noreferrer"),
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
