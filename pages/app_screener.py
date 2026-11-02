"""Live technical-rating screener for a selected set of FX pairs."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, dcc, html

from .side_bar import sidebar


dash.register_page(__name__, name="Market Screener", path="/app-screener", order=33)
_TIMEFRAMES = ["M5", "M15", "H1", "H4", "D1"]


def layout():
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(sidebar(), xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col(
                    [
                        html.H2("FOREX Market Screener", className="text-center"),
                        html.P("Scan the portfolio FX pairs using TradingView technical ratings. Results update when you refresh; automatic refresh is optional."),
                        dbc.Row(
                            [
                                dbc.Col([dbc.Label("Timeframe"), dcc.Dropdown(id="screener-timeframe", options=_TIMEFRAMES, value="D1", clearable=False)], md=3),
                                dbc.Col(dbc.Button("Refresh ratings", id="screener-refresh", n_clicks=0, color="info", className="w-100 mt-4"), md=3),
                                dbc.Col(dbc.Switch(id="screener-auto", label="Refresh every 5 minutes", value=False, className="mt-4"), md=4),
                            ],
                            className="g-3 align-items-end mb-3",
                        ),
                        dcc.Interval(id="screener-clock", interval=5 * 60 * 1000, n_intervals=0, disabled=True),
                        dbc.Alert("Choose a timeframe and refresh to fetch current ratings.", id="screener-status", color="secondary"),
                        dcc.Loading(html.Div(id="screener-table")),
                        html.P("Technical ratings are third-party indicators, can change rapidly, and are not investment advice.", className="small text-muted mt-3"),
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


@callback(Output("screener-clock", "disabled"), Input("screener-auto", "value"))
def toggle_screener_refresh(enabled):
    return not enabled


@callback(
    Output("screener-status", "children"),
    Output("screener-status", "color"),
    Output("screener-table", "children"),
    Input("screener-refresh", "n_clicks"),
    Input("screener-clock", "n_intervals"),
    State("screener-timeframe", "value"),
    prevent_initial_call=True,
)
def refresh_screener(refresh_clicks, interval_count, timeframe):
    try:
        from .def_symbols import get_symbol_names
        from .TradingViewTA import forex_scaner

        ratings = forex_scaner(get_symbol_names(), timeframe).reset_index()
        if ratings.empty:
            return "TradingView returned no ratings. Try again later.", "warning", None
        ratings.columns = ["Symbols", "Signal"]
        table = dash_table.DataTable(
            id="screener-ratings",
            data=ratings.to_dict("records"),
            columns=[{"name": column, "id": column} for column in ratings.columns],
            sort_action="native",
            filter_action="native",
            page_size=20,
            style_table={"overflowX": "auto"},
            style_cell={"backgroundColor": "#252b35", "color": "#f5f7fa", "textAlign": "center", "padding": "8px"},
            style_header={"backgroundColor": "#171b22", "fontWeight": "bold"},
            style_data_conditional=[
                {"if": {"filter_query": '{Signal} contains "BUY"', "column_id": "Signal"}, "color": "#42d392", "fontWeight": "bold"},
                {"if": {"filter_query": '{Signal} contains "SELL"', "column_id": "Signal"}, "color": "#ff6b6b", "fontWeight": "bold"},
            ],
        )
        return f"Loaded {len(ratings)} FX pair ratings for {timeframe}.", "success", table
    except Exception as exc:
        return f"Could not fetch market ratings: {exc}", "danger", None
