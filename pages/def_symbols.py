from tradingview_ta import Interval

def get_symbol_names():
    symbol_names = ["EURUSD", "AUDUSD", "USDCAD", "USDCHF", "AUDCAD", "CADCHF", "NZDUSD", "EURCAD", "AUDCHF", "GBPUSD",
         "GBPCAD", "GBPNZD", "AUDNZD", "EURGBP", "EURNZD", "GBPCHF", "EURCHF", "EURAUD", "NZDCAD", "NZDCHF", "GBPAUD",
        "GBPJPY", "CADJPY", "EURJPY", "AUDJPY", "NZDJPY","USDJPY","CHFJPY"]
    
    return symbol_names

#TIMEFRAMES = ['M1', 'M5', 'M15', 'M30', 'M45','H1', 'H4', 'D1', 'W1', 'MN1']
TIMEFRAMES = ['M5', 'M15', 'H1', 'H4', 'D1']
TIMEFRAME_DICT = {
    #'MN1' : Interval.in_monthly,
    #'W1' : Interval.in_weekly,
    'D1' : Interval.INTERVAL_1_DAY,
    'H4' : Interval.INTERVAL_4_HOURS,
    'H1' : Interval.INTERVAL_1_HOUR,
    'M15' : Interval.INTERVAL_15_MINUTES,
    'M5' : Interval.INTERVAL_5_MINUTES,
}

