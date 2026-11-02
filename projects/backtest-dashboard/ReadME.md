# Backtest Dashboard (copied project)

This folder contains a source copy of [raimiazeez26/BacktestDashboard](https://github.com/raimiazeez26/BacktestDashboard): the Dash application, backtesting module, original notebooks, dependency list, and Render configuration. Git metadata, IDE settings, and notebook checkpoint cache were omitted.

## Local run

From this folder, create and activate a virtual environment, install the listed requirements, then launch the dashboard:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/app.py
```

The original dependency file includes a Git-hosted `tvDatafeed` dependency. Installing that dependency requires network access and a compatible Python environment. The application fetches historical candles from TradingView data through `tvDatafeed`; upstream availability can affect the dashboard.

The dashboard is an educational backtesting tool, not investment advice. Historical simulations do not predict future performance.
