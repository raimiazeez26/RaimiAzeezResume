"""RA-StrategyLab portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="RA-StrategyLab", path="/project/ra-strategylab", order=30)

layout = lambda: render_project(
    title="RA-StrategyLab",
    category="AI & Quantitative Research",
    summary="Describe. Generate. Backtest. An AI-powered quantitative research platform that turns trading ideas written in plain English into executable, inspectable strategies and reproducible backtest results. AI interprets the idea; a deterministic engine calculates every number in the report.",
    features=[
        "Describe a strategy in plain English, answer clarifying questions, and get a validated specification and readable Python code with version history.",
        "Run generated and hand-written strategy code in an isolated sandbox (subprocess or Docker) with resource limits.",
        "Backtest on a deterministic bar engine with costs, stops and targets, long and short positions, sizing rules, a look-ahead audit and reproducible result hashes.",
        "Measure performance and risk, including Sharpe, Sortino, VaR/CVaR and drawdown, with trade and execution metrics.",
        "Test robustness with grid, random and Bayesian search, hold-out and walk-forward validation, overfitting warnings, Monte Carlo and regime analysis.",
        "Combine up to 10 strategies on shared capital with allocations, exposure limits, attribution and correlation.",
        "Pull market data from MT5, Binance, OANDA or CSV into immutable Parquet snapshots with quality reports.",
    ],
    technologies="Python, FastAPI, Celery, Redis, PostgreSQL, Next.js, TypeScript, OpenAI, Docker, Heroku",
    repository="https://github.com/raimiazeez26/RAStrategyLab",
    status="Deployed on Heroku (web app and API). Milestones M0–M7 plus optimisation, robustness and paper trading are built; live trading adapters are opt-in and off by default.",
    notes=[
        "No LLM output is ever used as a result: every reported figure comes from the deterministic engine.",
        "Paper trading keeps parity with the backtest engine; live trading sits behind an explicit opt-in, risk limits and a kill switch.",
    ],
    private=True,
    private_link=True,
    demo="https://ra-strategylab-web-51e6204d9730.herokuapp.com/",
)
