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

The app provides launcher pages for every externally submitted form-triggered
workflow found in the [n8n Client Onboarding workflow repository](https://github.com/raimiazeez26/n8n-client-onboarding):

- `/n8n-client-onboarding` — new client intake
- `/n8n-job-application` — record a new opportunity or application
- `/n8n-job-match` — request AI job and CV matching for an application ID
- `/n8n-application-status` — update an application's status

Each launcher opens the corresponding native n8n Form Trigger page. The client
onboarding follow-up and job application follow-up workflows use schedules and
do not need external form launchers.

Set `N8N_CLIENT_ONBOARDING_FORM_URL`, `N8N_JOB_APPLICATION_FORM_URL`,
`N8N_AI_MATCH_FORM_URL`, and `N8N_APPLICATION_STATUS_FORM_URL` to the active
Production URLs shown by their respective n8n Form Trigger nodes. For local
development, copy `.env.example` to `.env` and set each URL there. The app
loads `.env` on startup and accepts HTTPS URLs only. Unconfigured pages display
a setup message.

## Repository layout

```text
.
├── app.py                  # Dash app entry point and responsive navigation
├── Procfile                # Gunicorn deployment command
├── requirements.txt        # Python runtime dependencies
├── .env.example            # Local n8n form URL settings (no live URLs)
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

The repository is configured for Heroku's Python buildpack. The root-level
`.python-version` selects Python 3.14, `requirements.txt` installs the app's
dependencies, and the `web` process in `Procfile` starts the Dash WSGI server:

```text
gunicorn app:server --timeout 600
```

Deploy from the repository root and keep the app's configuration in Heroku
Config Vars. The form pages read these variables at runtime:

- `N8N_CLIENT_ONBOARDING_FORM_URL`
- `N8N_JOB_APPLICATION_FORM_URL`
- `N8N_AI_MATCH_FORM_URL`
- `N8N_APPLICATION_STATUS_FORM_URL`

Set each one to the active HTTPS Production URL from its n8n Form Trigger.
For example, using the Heroku CLI (replace each example URL with the matching
production URL):

```sh
heroku config:set N8N_CLIENT_ONBOARDING_FORM_URL="https://your-n8n-host/form/client-form-id" N8N_JOB_APPLICATION_FORM_URL="https://your-n8n-host/form/job-form-id" N8N_AI_MATCH_FORM_URL="https://your-n8n-host/form/match-form-id" N8N_APPLICATION_STATUS_FORM_URL="https://your-n8n-host/form/status-form-id"
```

Keep production URLs and credentials out of Git. Missing or invalid form URLs do
not prevent the app from starting; the relevant launcher page displays a setup
message instead.

After connecting the Heroku Git remote and setting Config Vars, deploy the
branch you intend to release, then check startup logs:

```sh
git push heroku main
heroku logs --tail
```

Heroku's router ends a synchronous web request after 30 seconds. The Gunicorn
worker timeout above does not extend that router limit, so live market scans or
backtests that take longer may return a timeout. See [Heroku's request timeout
guidance](https://devcenter.heroku.com/articles/request-timeout).

The Python 3.14 runtime in `.python-version` is supported by the [Heroku Python
buildpack](https://devcenter.heroku.com/articles/python-support). Heroku's
buildpack installs the dependencies from `requirements.txt` and uses the
`web` command from `Procfile`.

## Maintenance notes

- Do not commit `__pycache__/`, `*.py[cod]`, virtual environments, or local environment files.
- Keep Dash, Flask, Werkzeug, NumPy, SciPy, scikit-learn, statsmodels, and pmdarima versions mutually compatible.
- Prefer bounded network calls, explicit data validation, and user-facing handling for upstream data failures.
- GitHub Actions installs the declared requirements, compiles the app modules, and smoke-tests Dash startup.
- Move legacy modules out of auto-discovered `pages/` or remove them only after confirming they are not in use.

## License and data attribution

This repository contains third-party packages and sample datasets. Review the relevant package and dataset licenses before redistribution or commercial use.
