from tradingview_ta import TA_Handler, Interval, Exchange
from .def_symbols import get_symbol_names, TIMEFRAMES, TIMEFRAME_DICT
import pandas as pd

def get_signal(symbol, timeframe, screener, exchange):
    signal = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=timeframe,
            # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
        )
    
    return signal.get_analysis().summary

def forex_scaner(symbols, timeframe):
    
    screener = "forex"
    exchange = "FX_IDC"

    # Create an empty dictionary to store the results
    results = {}

#for timeframe in timeframes:
    for symbol in symbols:
        signal = get_signal(symbol, TIMEFRAME_DICT[timeframe], screener, exchange)

        if timeframe not in results:
            results[timeframe] = {}

        results[timeframe][symbol] = signal['RECOMMENDATION']

    # Convert the results dictionary to a pandas DataFrame
    results_df = pd.DataFrame(results)
    return results_df

