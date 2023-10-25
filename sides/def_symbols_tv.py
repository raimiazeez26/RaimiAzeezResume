from tvDatafeed import TvDatafeed, Interval

username = 'contactus@xaviermcallister.com'
password = 'xaviermcallister2019!!'
tv = TvDatafeed(username=username, password=password)

def get_symbol_names():
    symbol_names = ["EURUSD", "AUDUSD", "USDCAD", "USDCHF", "AUDCAD", "CADCHF", "NZDUSD", "EURCAD", "AUDCHF", "GBPUSD",
         "GBPCAD", "GBPNZD", "AUDNZD", "EURGBP", "EURNZD", "GBPCHF", "EURCHF", "EURAUD", "NZDCAD", "NZDCHF", "GBPAUD",
        "GBPJPY", "CADJPY", "EURJPY", "AUDJPY", "NZDJPY","USDJPY","CHFJPY"]
    
    return symbol_names

TIMEFRAMES = ['M1', 'M5', 'M15', 'M30', 'M45','H1', 'H4', 'D1', 'W1', 'MN1']
TIMEFRAME_DICT = {
    'MN1' : Interval.in_monthly,
    'W1' : Interval.in_weekly,
    'D1' : Interval.in_daily,
    'H4' : Interval.in_4_hour,
    'H1' : Interval.in_1_hour,
    'M45' : Interval.in_45_minute,
    'M30' : Interval.in_30_minute,
    'M15' : Interval.in_15_minute,
    'M5' : Interval.in_5_minute,
    'M1' : Interval.in_1_minute,
}

