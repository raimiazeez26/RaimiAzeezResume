"""Embedded, interactive FX strategy backtesting page."""

from pathlib import Path
import sys

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html
from ta import add_all_ta_features

from .market_data import get_market_data
from .side_bar import sidebar

_ENGINE_PATH = Path(__file__).resolve().parents[1] / "projects" / "backtest-dashboard" / "src"
if str(_ENGINE_PATH) not in sys.path:
    sys.path.insert(0, str(_ENGINE_PATH))

from Backtests import Strategy, signal  # noqa: E402

dash.register_page(__name__, name="Backtest Dashboard", path="/app-backtest", order=30)

_SYMBOLS = [
    "EURCAD", "AUDUSD", "USDCAD", "USDCHF", "AUDCAD", "CADCHF", "NZDUSD", "AUDCHF", "GBPUSD",
    "GBPCAD", "GBPNZD", "AUDNZD", "EURGBP", "EURNZD", "GBPCHF", "EURCHF", "EURAUD", "NZDCAD",
    "NZDCHF", "GBPAUD", "GBPJPY", "CADJPY", "EURJPY", "AUDJPY", "NZDJPY", "USDJPY", "CHFJPY",
]
_TIMEFRAMES = ["M1", "M5", "M15", "M30", "M45", "H1", "H4", "D1", "W1", "MN1"]
_INDICATORS = [
    "Open", "High", "Low", "Close", "Volume", "trend_sma_fast", "trend_sma_slow",
    "trend_ema_fast", "trend_ema_slow", "trend_macd", "trend_macd_signal", "trend_macd_diff",
    "trend_adx", "momentum_rsi", "momentum_stoch", "momentum_stoch_signal", "volatility_bbm",
    "volatility_bbh", "volatility_bbl", "volatility_atr", "volume_obv", "volume_mfi",
]
_OPERATORS = [
    "greater than", "greater than or equal to", "less than", "less than or equal to", "equal to",
]


def _rule_controls(prefix, label):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(label),
                dbc.Row(
                    [
                        dbc.Col([dbc.Label("First indicator"), dcc.Dropdown(id=f"btd-{prefix}-left", options=_INDICATORS, value="trend_ema_fast", clearable=False)], md=3),
                        dbc.Col([dbc.Label("Condition"), dcc.Dropdown(id=f"btd-{prefix}-operator", options=_OPERATORS, value="greater than", clearable=False)], md=3),
                        dbc.Col([dbc.Label("Compare against"), dcc.Dropdown(id=f"btd-{prefix}-type", options=["Indicator", "Value"], value="Indicator", clearable=False)], md=2),
                        dbc.Col([dbc.Label("Second indicator"), dcc.Dropdown(id=f"btd-{prefix}-right", options=_INDICATORS, value="trend_ema_slow", clearable=False)], md=2),
                        dbc.Col([dbc.Label("Numeric value"), dbc.Input(id=f"btd-{prefix}-value", type="number", value=0, step="any")], md=2),
                    ],
                    className="g-2",
                ),
            ]
        ),
        className="mb-3",
    )


def layout():
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(sidebar(), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col(
                    [
                        html.H2("Backtest Dashboard", className="text-center"),
                        html.P(
                            "Configure indicator rules and risk limits, then run them against historical OANDA candles. "
                            "This is a research tool; backtests are not investment advice and do not predict future results.",
                            className="mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col([dbc.Label("FX pair"), dcc.Dropdown(id="btd-symbol", options=_SYMBOLS, value="GBPUSD", clearable=False)], md=3),
                                dbc.Col([dbc.Label("Timeframe"), dcc.Dropdown(id="btd-timeframe", options=_TIMEFRAMES, value="H1", clearable=False)], md=2),
                                dbc.Col([dbc.Label("Stop loss (pips)"), dbc.Input(id="btd-stop", type="number", min=1, max=1000, value=10)], md=2),
                                dbc.Col([dbc.Label("Take profit (pips)"), dbc.Input(id="btd-target", type="number", min=1, max=1000, value=50)], md=2),
                                dbc.Col(dbc.Button("Run backtest", id="btd-run", n_clicks=0, color="info", className="w-100 mt-4"), md=3),
                            ],
                            className="g-3 align-items-end mb-3",
                        ),
                        _rule_controls("buy", "Buy entry rule"),
                        _rule_controls("sell", "Sell entry rule"),
                        dbc.Alert(
                            "Set your rules and run a backtest. Historical candles are fetched when you click the button.",
                            id="btd-status",
                            color="secondary",
                        ),
                        dcc.Loading(dcc.Graph(id="btd-equity-chart", figure=go.Figure(), config={"displayModeBar": False})),
                        html.Div(id="btd-metrics", className="mb-3"),
                        html.H4("Trade results"),
                        html.Div(id="btd-trades"),
                    ],
                    xs=8,
                    sm=8,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                    className="p-3",
                ),
            ],
            className="g-0",
        ),
        fluid=True,
    )


def _metrics(trades, starting_balance):
    net = pd.to_numeric(trades["Net Profit"], errors="coerce").fillna(0)
    gains = net[net > 0].sum()
    losses = abs(net[net < 0].sum())
    equity = trades["pnl"].astype(float)
    drawdown = equity / equity.cummax() - 1
    values = [
        ("Trades", len(trades)),
        ("Net profit", f"{net.sum():,.2f}"),
        ("Return", f"{net.sum() / starting_balance * 100:.2f}%"),
        ("Win rate", f"{(net > 0).mean() * 100:.1f}%"),
        ("Profit factor", f"{gains / losses:.2f}" if losses else ("∞" if gains else "—")),
        ("Max drawdown", f"{abs(drawdown.min()) * 100:.2f}%"),
    ]
    return dbc.Row(
        [
            dbc.Col(dbc.Card(dbc.CardBody([html.Div(name, className="small text-muted"), html.H5(value, className="mb-0")])), xs=6, md=4, lg=2, className="mb-2")
            for name, value in values
        ]
    )


@callback(
    Output("btd-status", "children"),
    Output("btd-status", "color"),
    Output("btd-equity-chart", "figure"),
    Output("btd-metrics", "children"),
    Output("btd-trades", "children"),
    Input("btd-run", "n_clicks"),
    State("btd-symbol", "value"),
    State("btd-timeframe", "value"),
    State("btd-stop", "value"),
    State("btd-target", "value"),
    State("btd-buy-left", "value"),
    State("btd-buy-operator", "value"),
    State("btd-buy-type", "value"),
    State("btd-buy-right", "value"),
    State("btd-buy-value", "value"),
    State("btd-sell-left", "value"),
    State("btd-sell-operator", "value"),
    State("btd-sell-type", "value"),
    State("btd-sell-right", "value"),
    State("btd-sell-value", "value"),
    prevent_initial_call=True,
)
def run_dashboard_backtest(n_clicks, symbol, timeframe, stop_loss, take_profit,
                           buy_left, buy_operator, buy_type, buy_right, buy_value,
                           sell_left, sell_operator, sell_type, sell_right, sell_value):
    if not n_clicks:
        return "Click Run backtest to begin.", "secondary", go.Figure(), None, None
    try:
        if not stop_loss or not take_profit or float(stop_loss) <= 0 or float(take_profit) <= 0:
            raise ValueError("Stop loss and take profit must both be positive pip values.")
        candles = get_market_data(symbol, timeframe, bars=6000)
        candles = candles.reset_index()
        if "datetime" not in candles.columns:
            candles = candles.rename(columns={candles.columns[0]: "datetime"})
        if "Volume" not in candles:
            candles["Volume"] = 0.0
        candles = add_all_ta_features(candles, open="Open", high="High", low="Low", close="Close", volume="Volume")
        candles = candles.replace([float("inf"), float("-inf")], pd.NA).dropna(subset=["Open", "High", "Low", "Close"])
        signals = signal(
            candles,
            buy_type,
            buy_operator,
            buy_left,
            buy_right if buy_type == "Indicator" else buy_value,
            sell_type,
            sell_operator,
            sell_left,
            sell_right if sell_type == "Indicator" else sell_value,
        )
        starting_balance = 100000.0
        strategy = Strategy(
            signals,
            starting_balance,
            float(stop_loss),
            float(take_profit),
            pip_size=0.01 if symbol.endswith("JPY") else 0.0001,
        )
        trades = strategy.run()
        if trades.empty:
            return "No trades matched those rules in the available history. Try different entry conditions or a longer timeframe.", "warning", go.Figure(), None, None

        chart = go.Figure(
            go.Scatter(x=trades["close_datetime"], y=trades["pnl"], mode="lines+markers", name="Account equity")
        )
        chart.update_layout(title=f"{symbol} · {timeframe} equity after each closed trade", xaxis_title="Close time", yaxis_title="Balance", template="plotly_dark", margin=dict(l=20, r=20, t=55, b=20))
        metrics = _metrics(trades, starting_balance)
        columns = ["open_datetime", "close_datetime", "order_type", "open_price", "close_price", "sl", "tp", "Net Profit", "pnl"]
        display = trades[columns].copy()
        for column in ("open_datetime", "close_datetime"):
            display[column] = pd.to_datetime(display[column]).dt.strftime("%Y-%m-%d %H:%M")
        for column in ("open_price", "close_price", "sl", "tp", "Net Profit", "pnl"):
            display[column] = pd.to_numeric(display[column], errors="coerce").round(5)
        table = dash_table.DataTable(
            id="btd-trades-table",
            columns=[{"name": name.replace("_", " ").title(), "id": name} for name in columns],
            data=display.to_dict("records"),
            page_size=15,
            sort_action="native",
            filter_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"backgroundColor": "#252b35", "color": "#f5f7fa", "textAlign": "left", "padding": "8px", "minWidth": "110px"},
            style_header={"backgroundColor": "#171b22", "fontWeight": "bold"},
        )
        status = f"Completed: {len(trades):,} closed trades from {len(candles):,} historical candles."
        return status, "success", chart, metrics, table
    except Exception as exc:
        return f"Backtest could not run: {exc}", "danger", go.Figure(), None, None
