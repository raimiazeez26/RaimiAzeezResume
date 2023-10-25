import pandas as pd
import numpy as np
from datetime import datetime as dt
from ta.trend import EMAIndicator
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()


# function to pull data
def get_data(symbol, timeframe, ema_slow, ema_fast):
    df = tv.get_hist(symbol=symbol, exchange='OANDA', interval=timeframe, n_bars=350)  # Interval.in_1_hour

    # create DataFrame out of the obtained data
    df = pd.DataFrame(df)
    # convert time in seconds into the datetime format
    df['time'] = pd.to_datetime(df.index, unit='s')
    # df.index = df.time.values
    df = df.drop(["symbol"], axis=1)  # "open", "high", "low"
    df = df.rename(columns={"open": "Open",
                            "close": "Close",
                            "high": "High",
                            "low": "Low",
                            "volume": "Volume"})

    df = df.reset_index()

    # ema_slow
    ema_slow = EMAIndicator(close=df.Close, window=ema_slow)
    df["ema_slow"] = round(ema_slow.ema_indicator(), 5)

    # ema_fast
    ema_fast = EMAIndicator(close=df.Close, window=ema_fast)
    df["ema_fast"] = round(ema_fast.ema_indicator(), 5)

    df = df.dropna()

    return df


def price_chart2(symbol, timeframe, ema_slow, ema_fast, plot_type):

    vhf_data = get_data(symbol, timeframe, ema_slow, ema_fast)
    print(vhf_data)
    plot_data = []
    if plot_type == 'candle':
        plot_data = go.Candlestick(
            x=vhf_data.datetime,
            open=vhf_data['Open'],
            high=vhf_data['High'],
            low=vhf_data['Low'],
            close=vhf_data['Close']
        )
    else:
        plot_data = go.Scatter(
            x=vhf_data.datetime,
            y=vhf_data['Close'],
            line={'color': 'black', 'width': 2},
            # marker = 'o',
            mode='lines',
            name='ema_slow')

    fig = go.Figure(data=[plot_data])
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  # hide weekends
        ])
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(yaxis_title='Price'
                      )
    fig.update_layout(xaxis_title='Date')

    return fig

def price_chart(symbol, timeframe, ema_slow, ema_fast, plot_type):
    vhf_data = get_data(symbol, timeframe, ema_slow, ema_fast)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    plot_data = []
    if plot_type == 'candle':
        # include candlestick with rangeselector
        fig.add_trace(go.Candlestick(x=vhf_data.datetime,
                                   open=vhf_data['Open'],
                                   high=vhf_data['High'],
                                   low=vhf_data['Low'],
                                   close=vhf_data['Close']),
                                    secondary_y=True)

    else:
        fig.add_trace(go.Scatter(x=vhf_data.datetime, y=vhf_data['Close'],
                               line={'color': 'black', 'width': 2},
                               # marker = 'o',
                               mode='lines',
                               name='ema_slow'),
                                secondary_y=True)


    fig.add_trace(go.Scatter(x=vhf_data.datetime, y=vhf_data["ema_slow"],
                             line={'color': 'blue', 'width': 1},
                             #marker = '',
                             mode='lines',
                             name='ema_slow'), secondary_y=True)

    fig.add_trace(go.Scatter(x=vhf_data.datetime, y=vhf_data["ema_fast"],
                             line={'color': 'yellow', 'width': 1},
                             # marker = 'o',
                             mode='lines', name='ema_fast'), secondary_y=True)

    # From our Dataframe take only the rows where the Close > Open
    # save it in different Dataframe, these should be green
    green_volume_df = vhf_data[vhf_data['Close'] > vhf_data['Open']]
    # Same for Close < Open, these are red candles/bars
    red_volume_df = vhf_data[vhf_data['Close'] < vhf_data['Open']]

    #include a go.Bar trace for volumes
    fig.add_trace(
        go.Bar(x=red_volume_df.datetime, y=red_volume_df['Volume'], name='Sell Volume', marker_color='#e0afaf'),
        # e0afaf #ef5350 #c2493e
        secondary_y=False)

    fig.add_trace(
        go.Bar(x=green_volume_df.datetime, y=green_volume_df['Volume'], name='Buy Volume', marker_color='#b5d1b2'),
        # b5d1b2 #26a69a #218560
        secondary_y=False)

    fig.layout.yaxis2.showgrid = False
    fig.layout.yaxis.showticklabels = False
    fig.update_xaxes(showgrid=False, showspikes=True, rangebreaks=[
        dict(bounds=["sat", "mon"])  # hide weekends
    ])

    fig.update(layout_xaxis_rangeslider_visible=False)

    # fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', uirevision="Don't change")

    fig.update_yaxes(showgrid=False, showspikes=False)

    fig.update_layout(
        height=600,
        margin=dict(l=50, r=20, t=50, b=50),
        showlegend=False,
        # yaxis={'side': 'right'},
        # yaxis2 = False
        # title_text=f"Price & VFH({lookback})",
    )

    return fig


# function to pull data
def get_price(symbol):
    df = tv.get_hist(symbol=symbol, exchange='OANDA', interval=Interval.in_1_hour, n_bars=5)  # Interval.in_1_hour

    # create DataFrame out of the obtained data
    df = pd.DataFrame(df)
    # convert time in seconds into the datetime format
    df['time'] = pd.to_datetime(df.index, unit='s')
    df.index = df.time.values
    df = df.drop(["time", "symbol"], axis=1)  # "open", "high", "low"
    df = df.rename(columns={"open": "Open",
                            "close": "Close",
                            "high": "High",
                            "low": "Low",
                            "volume": "Volume"})
    df = df.dropna()
    df = df.reset_index()['Close'].iloc[-1]

    return df


def calc_lot_size(symbol, account_currency, account_balance, risk, stop_loss_points):
    # get account currency
    # account_currency=mt5.account_info().currency

    # risk in currency amount
    risk_perc = float(risk)  # int(input("Input risk amout in percentage: ")) #%
    risk = (account_balance * risk_perc) / 100
    # print("Risk Amount = $", risk)

    # CALCULATE LOTSIZE FOR PAIRS WITH SAME ACCOUNTCURRENCY AS QUOTE
    if symbol[3:] == account_currency:

        lot = round(risk / stop_loss_points, 2)

    else:

        value_symbol = str(account_currency + symbol[3:])
        value_symbol2 = str(symbol[3:] + account_currency)
        try:
            pip_value = get_price(value_symbol)
        except:
            pip_value = get_price(value_symbol2)
        # print(f'Conversion symbol: {value_symbol} Price: {pip_value}')

        if 'JPY' in symbol:
            lot = round(((pip_value * risk) / stop_loss_points) / 100, 2)

        else:
            lot = round((pip_value * risk) / stop_loss_points, 2)

    return lot
