"""EMA Crossover + VWAP trading system portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="EMA Crossover + VWAP Trading System", path="/project/ema-vwap-trading-system", order=39)

layout = lambda: render_project(
    title="EMA Crossover + VWAP Trading System",
    category="Quant & Financial Engineering",
    summary="A multi-timeframe trend strategy that combines an EMA 8/13/21 stack with VWAP, RSI, and ROC filters. An MT5 pipeline backtests and optimizes parameters per symbol, and an OANDA bot trades the optimized parameters live.",
    features=[
        "Require EMA alignment on both trend and entry timeframes, price on the right side of VWAP, and agreeing RSI and ROC.",
        "Place pending stop orders beyond swing points, with ATR-buffered stop losses and risk-reward take profits.",
        "Size positions from account balance and stop distance, and cancel pending orders when price moves against the plan.",
        "Backtest and optimize on MT5 history, exporting the latest parameters per symbol.",
        "Run live on OANDA with state persistence, trade and order sync, weekend handling, and end-of-day reports.",
        "Send Telegram notifications and monitor operations from a dashboard.",
    ],
    technologies="Python, MetaTrader 5, OANDA v20 API, TA-Lib, pandas, Telegram Bot API, Dash, Heroku",
    repository="https://github.com/raimiazeez26/EMA_Crossover_VWAP_Strategy-v2",
    status="Backtest pipeline and live OANDA bot implemented; parameters refresh from the latest optimization outputs.",
    notes=[
        "Broker and Telegram credentials load from environment variables and are not stored in the repository.",
    ],
)
