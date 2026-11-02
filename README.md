# Raimi Azeez Babatunde — Interactive Resume & Analytics

A multi-page Dash application presenting Raimi Azeez Babatunde's professional profile and selected data science, financial engineering, and analytics demonstrations.

## Application

- **Framework:** Plotly Dash
- **UI:** Dash Bootstrap Components and Dash Bootstrap Templates
- **Charts and analysis:** Plotly, pandas, NumPy, scikit-learn, statsmodels, pmdarima, arch, Matplotlib, and `ta`
- **Market data:** TradingView through the `tvDatafeed` dependency; indicator pages also use `tradingview-ta`
- **Production server:** Gunicorn (`Procfile`)

The application is a collection of educational and portfolio demonstrations. Live market pages require a working network connection and an available TradingView data feed. Third-party services can change their interfaces or restrict access, so live data availability is not guaranteed.

## Pages and demonstrations

Dash Pages discovers user-facing modules under `pages/`. Current examples include:

- Profile/about and resume pages
- ARIMA time-series forecasting
- GARCH volatility analysis
- Black–Scholes option pricing
- K-means customer segmentation
- Northwind sales dashboard
- COVID-19 timeline visualization
- Amortization schedule
- Forex technical-analysis signals
- Live chart and position sizing

The repository also contains older or alternative modules under `sides/` and non-page helper modules. Those files are retained for project history and are not all exposed as app routes.

## Repository layout

```text
.
├── app.py                  # Dash app entry point and responsive navigation
├── Procfile                # Gunicorn deployment command
├── requirements.txt        # Python runtime dependencies
├── assets/                 # Sample datasets and images
├── pages/                  # Dash pages and analysis helpers
└── sides/                  # Legacy/alternative dashboard modules
```

ARIMA and GARCH retrieve OHLC candles on demand through `pages/market_data.py`; they do not require a checked-in `forex_data.csv`. Dashboard datasets are loaded from `assets/` using paths relative to their modules.

## Run locally

Use a Python environment compatible with the pinned packages in `requirements.txt`.

1. Clone the repository and enter its directory:
   ```bash
   git clone https://github.com/raimiazeez26/RaimiAzeezResume.git
   cd RaimiAzeezResume
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:8050`.

For a production-style local launch, install the requirements and run `gunicorn app:server`. The `PORT` environment variable is used by the local Dash entry point.

## Data and external services

- The Northwind dashboard and clustering demonstrations use sample files in `assets/`.
- ARIMA and GARCH request recent candles when a user selects a symbol and timeframe. If TradingView is unavailable, the shared helper raises a descriptive `MarketDataError`.
- Forex signal and live chart pages also call third-party market-data services. Network, rate limits, or upstream changes can affect those pages independently of app startup.
- Keep credentials out of source files. A historical TradingView credential example was present in a comment in the original source. Rotate any credential that was real and committed.

## Deployment

The included `Procfile` starts the WSGI server with:

```text
gunicorn app:server --timeout 600
```

Configure the hosting service to install `requirements.txt` and use the repository root as the working directory. Confirm the platform's Python version explicitly; the dependency pins are old and should be refreshed and tested before choosing a newer runtime.

## Maintenance notes

- Do not commit `__pycache__/`, `*.py[cod]`, virtual environments, or local environment files.
- Keep Dash, Flask, Werkzeug, NumPy, SciPy, scikit-learn, statsmodels, and pmdarima versions mutually compatible.
- Prefer bounded network calls, explicit data validation, and user-facing handling for upstream data failures.
- Validate every page after dependency changes. A lightweight CI workflow should compile Python files, install the declared requirements, and smoke-test app startup.
- Move legacy modules out of auto-discovered `pages/` or remove them only after confirming they are not in use.

## License and data attribution

This repository contains third-party packages and sample datasets. Review the relevant package and dataset licenses before redistribution or commercial use.
