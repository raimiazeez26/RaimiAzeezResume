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
- A client intake form that forwards submissions to the n8n Client Onboarding main workflow

The repository also contains older or alternative modules under `sides/` and non-page helper modules. Those files are retained for project history and are not all exposed as app routes.

## n8n Client Onboarding form

The `/n8n-client-onboarding` page embeds the main workflow's hosted Form Trigger
from the [n8n Client Onboarding workflow repository](https://github.com/raimiazeez26/n8n-client-onboarding).
The follow-up workflow is schedule-triggered and does not need a separate form.
The embedded form contains the required client name, email, company, service,
project description, and demo-data acknowledgment fields, with optional phone,
company size, industry, start date, budget, and contact preference.

Set `N8N_CLIENT_ONBOARDING_FORM_URL` to the active Production URL shown by the
n8n Form Trigger. For local development, copy `.env.example` to `.env` and
set the URL there. The app loads `.env` on startup. The URL must use HTTPS.
Without this setting, the page displays a configuration message.

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

Use Python 3.14, as declared in `.python-version`, and install the compatible
dependencies listed in `requirements.txt`.

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

Configure the hosting service to install `requirements.txt`, use the repository root as the working directory, and set `N8N_CLIENT_ONBOARDING_WEBHOOK_URL` as a server-side config variable. Keep this value private. The supported Python runtime is recorded in `.python-version`.

## Maintenance notes

- Do not commit `__pycache__/`, `*.py[cod]`, virtual environments, or local environment files.
- Keep Dash, Flask, Werkzeug, NumPy, SciPy, scikit-learn, statsmodels, and pmdarima versions mutually compatible.
- Prefer bounded network calls, explicit data validation, and user-facing handling for upstream data failures.
- GitHub Actions installs the declared requirements, compiles the app modules, and smoke-tests Dash startup.
- Move legacy modules out of auto-discovered `pages/` or remove them only after confirming they are not in use.

## License and data attribution

This repository contains third-party packages and sample datasets. Review the relevant package and dataset licenses before redistribution or commercial use.
