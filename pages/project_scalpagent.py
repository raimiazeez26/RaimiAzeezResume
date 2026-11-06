"""ScalpAgent portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="ScalpAgent", path="/project/scalpagent", order=38)

layout = lambda: render_project(
    title="ScalpAgent",
    category="Quant & Financial Engineering",
    summary="A short-horizon scalping runtime with a browser dashboard, multi-broker adapters, cost-aware risk controls, and managed exits. A deterministic replay harness runs the exact live logic bar by bar, and a parallel optimizer tunes parameters per symbol.",
    features=[
        "Trade through paper, MetaTrader 5, OANDA, and Hyperliquid adapters with multi-account support.",
        "Score long and short setups from indicator frames and apply cost-aware risk gating and position sizing.",
        "Manage exits with break-even and trailing stops, timeouts, opposite-signal and invalidation rules, and bar-based cooldowns.",
        "Operate from a FastAPI dashboard with runtime controls, live and closed trades, a decision log, and an emergency close.",
        "Replay historical bars through the live runtime logic and export every decision, score, and risk check to CSV.",
        "Grid-search parameters in parallel with a composite score and validate them out of sample.",
    ],
    technologies="Python, FastAPI, SQLite, MetaTrader 5, OANDA, Hyperliquid, JavaScript",
    repository="https://github.com/raimiazeez26/ScalpAgent",
    status="Working runtime with replay, optimization, and a unit test suite; versioned parameter sets for BTC, XAU, and EUR.",
    notes=[
        "Trades, decisions, and runtime logs are persisted to SQLite for reconciliation and review.",
    ],
    private=True,
)
