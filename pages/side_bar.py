"""Grouped left navigation for portfolio, data science, AI, and quant work."""

import dash
import dash_bootstrap_components as dbc
from dash import html


def sidebar():
    """Render registered app pages in project-type groups."""
    page_by_path = {page["path"]: page for page in dash.page_registry.values()}
    groups = [
        (
            "Portfolio",
            [("About", "/"), ("Projects", "/projects"), ("Resume", "/resume")],
        ),
        (
            "Data Science & Analytics",
            [
                ("K-Means Clustering", "/app-clustering"),
                ("Northwind Dashboard", "/app-northwind"),
                ("COVID-19 Timeline", "/app-covid"),
                ("BudgetMe", "/project/budgetme"),
            ],
        ),
        (
            "AI & Automation",
            [
                ("Client Onboarding", "/n8n-client-onboarding"),
                ("Job Application Form", "/n8n-job-application"),
                ("AI Job Match", "/n8n-job-match"),
                ("Application Status", "/n8n-application-status"),
                ("AI Financial Analyst App", "/app-aianalyist"),
                ("RAIMI-ANALYST", "/app-tagpt"),
                ("Content Forge", "/project/content-forge"),
                ("AI Research Workflow", "/project/ai-financial-analyst"),
                ("Boardroom AI v2", "/project/boardroom-ai"),
                ("RAI Automations", "/project/rai-automations"),
            ],
        ),
        (
            "Quant & Financial Engineering",
            [
                ("ARIMA Forecasting", "/app-arima"),
                ("GARCH Volatility", "/app-garch"),
                ("Black-Scholes Option Pricing", "/app-blackscholes"),
                ("Forex Trading Signals", "/app-forexsignal"),
                ("Market Screener", "/app-screener"),
                ("Live Chart & Position Sizing", "/app-live-chart-window"),
                ("Amortization Schedule", "/app-amortization"),
                ("Backtest Dashboard", "/app-backtest"),
                ("NGX Market Intelligence", "/project/ngx-market-intelligence"),
                ("NGX Short-Horizon Alpha", "/project/ngx-short-horizon-alpha"),
                ("ScalpAgent", "/project/scalpagent"),
                ("EMA + VWAP Trading System", "/project/ema-vwap-trading-system"),
            ],
        ),
    ]

    children = []
    for group_title, links in groups:
        group_items = [
            (label, path)
            for label, path in links
            if path in page_by_path
        ]
        if not group_items:
            continue
        children.append(
            html.Div(
                group_title,
                className="text-uppercase text-secondary small fw-bold px-3 pt-3 pb-1",
            )
        )
        children.extend(
            dbc.NavLink(label, href=path, active="exact", className="py-2")
            for label, path in group_items
        )

    return dbc.Nav(
        children,
        vertical=True,
        pills=True,
        className="bg-dark rounded h-100",
    )
