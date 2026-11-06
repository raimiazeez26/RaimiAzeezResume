"""NGX Short-Horizon Alpha portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="NGX Short-Horizon Alpha", path="/project/ngx-short-horizon-alpha", order=37)

layout = lambda: render_project(
    title="NGX Short-Horizon Alpha",
    category="Quant & Financial Engineering",
    summary="Reproducible research on whether technical, point-in-time fundamental, and macro information improve cross-sectional equity selection on the Nigerian Exchange (NGX). The study holds the model fixed and compares information sets, then tests the resulting portfolios against regional and global benchmarks.",
    features=[
        "Ingest NGX prices, company fundamentals, and macro inputs with point-in-time availability dates.",
        "Compare four information sets with a fixed HistGradientBoostingRegressor: technical, fundamental, technical plus fundamental, and all three with macro.",
        "Predict the cross-sectional rank of future total return and form a weekly, cost-aware top-quintile portfolio.",
        "Use expanding walk-forward folds so no fold sees future information.",
        "Report 5-, 10-, and 20-day primary horizons, with 40-, 60-, and 90-day robustness runs.",
        "Benchmark against NGX ASI, SPY, EEM, and EZA with block-bootstrap and Newey–West inference.",
    ],
    technologies="Python, scikit-learn, pandas, NumPy, statsmodels, walk-forward validation",
    repository="https://github.com/raimiazeez26/short_horizon_alpha_ngx",
    status="Research complete with a manuscript, summary results, and replication scripts. Raw market and statement data are licensed and kept local.",
    notes=[
        "A fundamentals-ledger validator checks point-in-time integrity before any model run.",
    ],
    private=True,
)
