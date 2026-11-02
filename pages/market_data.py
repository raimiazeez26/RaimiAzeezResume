"""Shared, validated access to TradingView candle data used by analysis pages."""

from functools import lru_cache

import pandas as pd
from tvDatafeed import TvDatafeed

from .def_symbols_tv import TIMEFRAME_DICT


class MarketDataError(RuntimeError):
    """Raised when historical market data cannot be retrieved or validated."""


@lru_cache(maxsize=1)
def _client():
    # Lazily create the client so importing the app does not perform network work.
    return TvDatafeed()


def get_market_data(symbol, timeframe, bars=1000):
    """Return normalized OHLCV candles for a supported symbol and timeframe."""
    if timeframe not in TIMEFRAME_DICT:
        supported = ", ".join(TIMEFRAME_DICT)
        raise ValueError(
            f"Unsupported timeframe {timeframe!r}. Choose one of: {supported}."
        )
    if not isinstance(bars, int) or bars < 2:
        raise ValueError("bars must be an integer greater than 1.")

    try:
        data = _client().get_hist(
            symbol=symbol,
            exchange="OANDA",
            interval=TIMEFRAME_DICT[timeframe],
            n_bars=bars,
        )
    except Exception as exc:
        raise MarketDataError(
            f"Unable to retrieve {symbol} {timeframe} candles from TradingView."
        ) from exc

    if data is None or data.empty:
        raise MarketDataError(
            f"No TradingView candle data is available for {symbol} {timeframe}."
        )

    data = data.copy()
    data.columns = [str(column).lower() for column in data.columns]
    required = {"open", "high", "low", "close"}
    missing = required.difference(data.columns)
    if missing:
        raise MarketDataError(
            "TradingView returned incomplete candle data; missing "
            + ", ".join(sorted(missing))
            + "."
        )

    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )
    data.index = pd.to_datetime(data.index, errors="coerce")
    data = data.loc[~data.index.isna()].sort_index()
    data = data.dropna(subset=["Open", "High", "Low", "Close"])

    if data.empty:
        raise MarketDataError(
            f"TradingView returned no valid OHLC candles for {symbol} {timeframe}."
        )
    if (data["Close"] <= 0).any():
        raise MarketDataError("Candle close prices must be positive.")

    return data
