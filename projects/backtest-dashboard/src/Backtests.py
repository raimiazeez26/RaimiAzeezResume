"""Historical market-data and rule-based FX backtest engine."""

from datetime import date

import numpy as np
import pandas as pd
from tvDatafeed import Interval, TvDatafeed


timeframe_tv = {
    "MN1": Interval.in_monthly,
    "W1": Interval.in_weekly,
    "D1": Interval.in_daily,
    "H4": Interval.in_4_hour,
    "H1": Interval.in_1_hour,
    "M45": Interval.in_45_minute,
    "M30": Interval.in_30_minute,
    "M15": Interval.in_15_minute,
    "M5": Interval.in_5_minute,
    "M1": Interval.in_1_minute,
}


def get_data(symbol, timeframe, exchange="OANDA", bars=6000):
    """Fetch and normalize OHLCV candles from TradingView."""
    if timeframe not in timeframe_tv:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    raw = TvDatafeed().get_hist(
        symbol=symbol,
        exchange=exchange,
        interval=timeframe_tv[timeframe],
        n_bars=bars,
    )
    if raw is None or raw.empty:
        raise ValueError(f"No market data returned for {symbol} ({timeframe}).")
    data = raw.reset_index()
    if "datetime" not in data.columns:
        data = data.rename(columns={data.columns[0]: "datetime"})
    data = data.rename(
        columns={
            "open": "Open",
            "close": "Close",
            "high": "High",
            "low": "Low",
            "volume": "Volume",
            "symbol": "Ticker",
        }
    )
    data["datetime"] = pd.to_datetime(data["datetime"], errors="coerce")
    return data.dropna(subset=["datetime", "Open", "High", "Low", "Close"]).reset_index(drop=True)


_OPERATORS = {
    "equal to": lambda left, right: left == right,
    "greater than": lambda left, right: left > right,
    "less than": lambda left, right: left < right,
    "greater than or equal to": lambda left, right: left >= right,
    "less than or equal to": lambda left, right: left <= right,
}


def _evaluate_rule(data, comparison_type, operator, left_name, right_value):
    if operator not in _OPERATORS:
        raise ValueError(f"Unsupported comparison operator: {operator}")
    if left_name not in data.columns:
        raise ValueError(f"Indicator {left_name!r} is not available in this candle data.")
    left = data[left_name]
    if comparison_type == "Indicator":
        if right_value not in data.columns:
            raise ValueError(f"Indicator {right_value!r} is not available in this candle data.")
        right = data[right_value]
    else:
        try:
            right = float(right_value)
        except (TypeError, ValueError) as exc:
            raise ValueError("A numeric comparison value is required.") from exc
    return _OPERATORS[operator](left, right).fillna(False)


def signal(data, buy_con_type, buy_con, buy_ind1, buy_ind2, sell_con_type, sell_con, sell_ind1, sell_ind2):
    """Add Buy, Sell, or Neutral signals from the configured entry rules."""
    result = data.copy()
    buy = _evaluate_rule(result, buy_con_type, buy_con, buy_ind1, buy_ind2)
    sell = _evaluate_rule(result, sell_con_type, sell_con, sell_ind1, sell_ind2)
    result["signal"] = np.select([buy, sell], ["Buy", "Sell"], default="Neutral")
    return result


class Position:
    """A single simulated long or short position."""

    def __init__(self, open_datetime, open_price, order_type, volume, sl, tp, commission):
        self.open_datetime = open_datetime
        self.open_price = float(open_price)
        self.order_type = order_type
        self.volume = float(volume)
        self.sl = float(sl)
        self.tp = float(tp)
        self.com = float(commission)
        self.close_datetime = None
        self.close_price = None
        self.profit = 0.0
        self.returns = 0.0
        self.status = "open"

    def close_position(self, close_datetime, close_price):
        self.close_datetime = close_datetime
        self.close_price = float(close_price)
        direction = 1 if self.order_type == "buy" else -1
        self.profit = (self.close_price - self.open_price) * self.volume * direction
        self.returns = direction * (self.close_price - self.open_price) / self.open_price
        self.status = "closed"

    def _asdict(self):
        return {
            "open_datetime": self.open_datetime,
            "open_price": self.open_price,
            "order_type": self.order_type,
            "volume": self.volume,
            "sl": self.sl,
            "tp": self.tp,
            "close_datetime": self.close_datetime,
            "close_price": self.close_price,
            "returns": self.returns,
            "profit": self.profit,
            "com": self.com,
            "Net Profit": self.profit + self.com,
            "status": self.status,
        }


class Strategy:
    """Simulate one open position at a time with stop-loss and take-profit exits."""

    def __init__(self, data, starting_balance, sl_pips, tp_pips, pip_size=0.0001, volume=100000, commission=7.0):
        self.starting_balance = float(starting_balance)
        self.positions = []
        self.data = data.reset_index(drop=True).copy()
        self.sl_pips = float(sl_pips)
        self.tp_pips = float(tp_pips)
        self.pip_size = float(pip_size)
        self.volume = float(volume)
        self.commission = float(commission)

    def get_positions_df(self):
        columns = [
            "open_datetime", "open_price", "order_type", "volume", "sl", "tp",
            "close_datetime", "close_price", "returns", "profit", "com", "Net Profit", "status", "pnl",
        ]
        if not self.positions:
            return pd.DataFrame(columns=columns)
        trades = pd.DataFrame([position._asdict() for position in self.positions])
        trades["pnl"] = trades["Net Profit"].cumsum() + self.starting_balance
        return trades

    def _has_open_position(self):
        return any(position.status == "open" for position in self.positions)

    def _close_on_bar(self, row):
        for position in self.positions:
            if position.status != "open":
                continue
            low = float(row["Low"])
            high = float(row["High"])
            if position.order_type == "buy":
                # For ambiguous candles that touch both barriers, assume the stop was hit first.
                if low <= position.sl:
                    position.close_position(row["datetime"], position.sl)
                elif high >= position.tp:
                    position.close_position(row["datetime"], position.tp)
            else:
                if high >= position.sl:
                    position.close_position(row["datetime"], position.sl)
                elif low <= position.tp:
                    position.close_position(row["datetime"], position.tp)

    def _open_from_signal(self, row):
        if self._has_open_position():
            return
        signal_value = row["signal"]
        if signal_value not in ("Buy", "Sell"):
            return
        side = "buy" if signal_value == "Buy" else "sell"
        price = float(row["Close"])
        direction = 1 if side == "buy" else -1
        stop = price - direction * self.sl_pips * self.pip_size
        target = price + direction * self.tp_pips * self.pip_size
        self.positions.append(
            Position(row["datetime"], price, side, self.volume, stop, target, -self.commission)
        )

    def run(self):
        if self.data.empty:
            return self.get_positions_df()
        required = {"datetime", "Open", "High", "Low", "Close", "signal"}
        missing = required.difference(self.data.columns)
        if missing:
            raise ValueError("Backtest input is missing: " + ", ".join(sorted(missing)))
        for _, row in self.data.iterrows():
            self._close_on_bar(row)
            self._open_from_signal(row)
        # Realize any position that remained open at the end of the selected history.
        last = self.data.iloc[-1]
        for position in self.positions:
            if position.status == "open":
                position.close_position(last["datetime"], last["Close"])
        return self.get_positions_df()
