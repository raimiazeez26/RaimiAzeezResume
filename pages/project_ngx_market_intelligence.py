"""NGX Market Intelligence portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="NGX Market Intelligence", path="/project/ngx-market-intelligence", order=33)

layout = lambda: render_project(
    title="NGX Market Intelligence",
    category="Quant & Financial Engineering",
    summary="A Nigerian equities analysis workspace pairing a FastAPI backend with a React and TypeScript dashboard. The planned product brings NGX stock prices, technical indicators, stock screening, portfolio exploration, and interactive charts together in one interface.",
    features=[
        "Browse stock information, historical price data, summaries, and screener results through API routes.",
        "Calculate technical indicators and directional summaries from market data.",
        "Explore React dashboard views for stock details, screening, charts, and portfolio allocation.",
        "Map NGX-listed symbols to TradingView's NSENG exchange data source.",
    ],
    technologies="Python, FastAPI, SQLAlchemy, React, TypeScript, Vite, pandas, TradingView data",
    repository="https://github.com/raimiazeez26/NGX-Market-Inteligence",
    status="Active development scaffold; the repository says the forecasting page is hidden and the predictive model remains pending.",
    notes=[
        "The repository is private, so the source link requires the owner's GitHub access.",
        "Production deployment depends on external market-data availability and a persistent database configuration.",
    ],
)
