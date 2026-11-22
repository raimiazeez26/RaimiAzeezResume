"""TradingPlayground portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="TradingPlayground", path="/project/trading-playground", order=29)

layout = lambda: render_project(
    title="TradingPlayground: RL Model Playground",
    category="Reinforcement Learning",
    summary="An evaluation environment for reinforcement-learning trading policies. Load an exported model, replay it bar by bar on market data it has never seen, and watch every decision pass through an independent risk engine and a simulated paper account. Each run ends with a full report, and sessions can be compared side by side.",
    features=[
        "Load Stable-Baselines3 policies (PPO, A2C, DQN, SAC, TD3, RecurrentPPO) from a validated model package, an HTTPS link, or a pinned Hugging Face Hub commit.",
        "Replay without look-ahead: the policy decides at each bar close and orders fill at the next bar's open.",
        "Route every action through risk rules the model cannot bypass, covering position size, exposure, leverage, per-trade and daily loss, drawdown, losing streaks and inference errors.",
        "Trace each decision from observation to model action, risk decision, order and fill in a live decision feed.",
        "Flag test windows that overlap the model's training data, and compare runs on whether they used the same data, execution assumptions and risk limits.",
        "Export HTML and PDF reports and CSV/JSON ledgers, or run headless from the command line.",
        "Train a reference policy in the included notebook and export it in the package format the Playground loads.",
    ],
    technologies="Python, Stable-Baselines3, PyTorch, Gymnasium, FastAPI, PostgreSQL, React, TypeScript, WebSocket, Docker",
    repository="https://github.com/raimiazeez26/TradingPlayground",
    status="Release 1 complete (milestones M0–M7 merged, user acceptance testing passed). Heroku deployment support is built; the public deployment is not live yet.",
    notes=[
        "Model files are opened only in an isolated worker process with no network access, a read-only filesystem and resource limits; the API never loads them.",
        "Paper trading only: there is no live order routing, and the paper_trading_only setting cannot be turned off.",
        "Sessions run in a background runner, recover after a crash without duplicate orders, and record every event of a decision under one correlation ID.",
    ],
    private=True,
    private_link=True,
)
