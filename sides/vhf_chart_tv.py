import pandas as pd
import numpy as np
from datetime import datetime as dt
from ta.trend import EMAIndicator
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tvDatafeed import TvDatafeed, Interval

username = 'contactus@xaviermcallister.com'
password = 'xaviermcallister2019!!'
tv = TvDatafeed(username=username, password=password)

#function to pull data 
def get_data(symbol, timeframe, ema_slow, ema_fast):
    df = tv.get_hist(symbol=symbol,exchange='OANDA' ,interval=timeframe, n_bars=500) #Interval.in_1_hour
    
    # create DataFrame out of the obtained data
    df = pd.DataFrame(df)
    # convert time in seconds into the datetime format
    df['time']=pd.to_datetime(df.index, unit='s')
    df.index = df.time.values
    df = df.drop(["time", "symbol"], axis = 1) #"open", "high", "low"
    df = df.rename(columns = {"open": "Open", 
                     "close": "Close",
                     "high": "High",
                     "low": "Low",
                     "volume": "Volume"})
    df = df.dropna()
    df = df.reset_index()
    
    #ema_slow
    ema_slow = EMAIndicator(close = df.Close, window = ema_slow)
    df["ema_slow"] = round(ema_slow.ema_indicator(), 5)
    
    #ema_fast
    ema_fast = EMAIndicator(close = df.Close, window = ema_fast)
    df["ema_fast"] = round(ema_fast.ema_indicator(), 5)
    
    return df

# Adds a specified number of columns in an array
def adder(Data, times):
    
    for i in range(1, times + 1):
    
        z = np.zeros((len(Data), 1), dtype = float)
        Data = np.append(Data, z, axis = 1)
    return Data
# Deletes a specified column in an array
def deleter(Data, index, times):
    
    for i in range(1, times + 1):
    
        Data = np.delete(Data, index, axis = 1)
    return Data
# Skips a certain number of rows in an array  
def jump(Data, jump):
    
    Data = Data[jump:, ]
    
    return Data

def vertical_horizontal_indicator(Data, lookback, what, where):
    
    Data = adder(Data, 4)
    
    for i in range(len(Data)):
        Data[i, where] = Data[i, what] - Data[i - 1, what]
    
    Data = jump(Data, 1) 
    
    Data[:, where] = abs(Data[:, where])
    for i in range(len(Data)):
        Data[i, where + 1] = Data[i - lookback + 1:i + 1, where].sum()
    
    for i in range(len(Data)):
        try:
            Data[i, where + 2] = max(Data[i - lookback + 1:i + 1, what]) - min(Data[i - lookback + 1:i + 1, what])
        except ValueError:
            pass
    Data = jump(Data, lookback)  
  
    Data[:, where + 3] = Data[:, where + 2] / Data[:, where + 1]
    
    Data = deleter(Data, where, 3)
    
    return Data

def get_vhf_data(symbol, timeframe, ema_slow, ema_fast):
    #symbol = "AUDCHF"
    lookback = 50
    close_col = 4
    vhf_col = 8
    my_data = get_data(symbol, timeframe, ema_slow, ema_fast)
    data = vertical_horizontal_indicator(my_data, lookback, close_col, vhf_col)
    vhf_data = pd.DataFrame(data)
    vhf_data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume','ema_slow', 'ema_fast', 'VHF']

    #ema
    ema = EMAIndicator(close = vhf_data.VHF, window = 10)
    vhf_data["VHF_EMA"] = round(ema.ema_indicator(), 5)
    vhf_data.dropna(inplace = True)

    return vhf_data

def vhf_levels(vhf_data, high, low):
    df_perc_high = np.percentile(vhf_data.VHF, high)
    df_perc_low = np.percentile(vhf_data.VHF, low)
    df_perc_mid = (max(vhf_data.VHF) + min(vhf_data.VHF))/2
    
    return(df_perc_low, df_perc_mid, df_perc_high)


def plot_subplots(symbol, timeframe, ema_slow, ema_fast):
    vhf_data = get_vhf_data(symbol, timeframe, ema_slow, ema_fast)
    levels = vhf_levels(vhf_data, 80,20)
    fig = make_subplots(
        rows=2, cols=1,
        row_heights = [600, 200],
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_titles = [None, "VHF(50)"],
        specs=[
               [{"type": "candlestick"}],
               [{"type": "scatter"}]]
        )
    
    

    fig.add_trace(go.Candlestick(x=vhf_data.Time,
                    open=vhf_data['Open'],
                    high=vhf_data['High'],
                    low=vhf_data['Low'],
                    close=vhf_data['Close'],
                    name='Price'),
        row=1, col=1
    )
    
    fig.add_trace(go.Scatter(x=vhf_data.Time,y=vhf_data["ema_slow"], name='ema_slow'), row=1, col=1)
    fig.add_trace(go.Scatter(x=vhf_data.Time,y=vhf_data["ema_fast"], name='ema_fast'), row=1, col=1)
    

    fig.add_trace(go.Scatter(x=vhf_data.Time, y= vhf_data.VHF,
                  line={'color':'blue', 'width':1},     
                  mode='lines',
                  name='VHF'),
                 row=2, col=1)
    
    fig.add_trace(go.Scatter(x=vhf_data.Time, y= vhf_data.VHF_EMA,
              line={'color':'red', 'width':1},
              #marker = 'o',
              mode='lines',
              name='VHF_EMA'),
        row=2, col=1
             )
    
    #fig.add_hline(y=levels[0], row=2, col=1)
    #fig.add_hline(y=levels[1], row=2, col=1)
    
    
    fig.update_layout(
        height=800,
        showlegend=False,
        yaxis={'side': 'right'}
        #title_text=f"Price & VFH({lookback})",
    )
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', uirevision="Don't change")
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_xaxes(showgrid=False, showspikes=True, rangebreaks=[
            dict(bounds=["sat", "mon"]) #hide weekends
        ])
    fig.update_yaxes(showgrid=False, showspikes=False) 

    

    #fig.show()
    return fig

def price_chart(symbol, timeframe, ema_slow, ema_fast):
    
    vhf_data = get_vhf_data(symbol, timeframe, ema_slow, ema_fast)
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=vhf_data.Time,
                        open=vhf_data['Open'],
                        high=vhf_data['High'],
                        low=vhf_data['Low'],
                        close=vhf_data['Close']),
                   secondary_y=True)
    
    fig.add_trace(go.Scatter(x=vhf_data.Time,y=vhf_data["ema_slow"], 
                             line={'color':'red', 'width':1},
                              #marker = 'o',
                              mode='lines',
                             name='ema_slow'), secondary_y=True)
    
    fig.add_trace(go.Scatter(x=vhf_data.Time,y=vhf_data["ema_fast"], 
                              line={'color':'green', 'width':1},
                              #marker = 'o',
                              mode='lines',name='ema_fast'), secondary_y=True)
    
    # From our Dataframe take only the rows where the Close > Open
    # save it in different Dataframe, these should be green
    green_volume_df = vhf_data[vhf_data['Close'] > vhf_data['Open']]
    # Same for Close < Open, these are red candles/bars
    red_volume_df = vhf_data[vhf_data['Close'] < vhf_data['Open']]

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=red_volume_df['Time'], y=red_volume_df['Volume']/100, name='Sell Volume', marker_color='#e0afaf'), #e0afaf #ef5350
                   secondary_y=False)

    fig.add_trace(go.Bar(x=green_volume_df['Time'], y=green_volume_df['Volume']/100, name='Buy Volume', marker_color='#b5d1b2'), #b5d1b2 #26a69a
                   secondary_y=False)

    fig.layout.yaxis2.showgrid=False
    fig.layout.yaxis.showticklabels=False
    fig.update_xaxes(showgrid=False, showspikes=True, rangebreaks=[
            dict(bounds=["sat", "mon"]) #hide weekends
        ])

    fig.update(layout_xaxis_rangeslider_visible=False)

    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', uirevision="Don't change")

    fig.update_yaxes(showgrid=False, showspikes=False) 

    fig.update_layout(
        height=500,
        showlegend=False,
        #yaxis={'side': 'right'},
        #yaxis2 = False
        #title_text=f"Price & VFH({lookback})",
    )
        
    #fig.update_yaxes(range=(200,1000))
    #fig.update_layout(yaxis2=dict(range=[200,1000]))
     
    #fig.show()
    return fig

def vhf_plot(symbol, timeframe, ema_slow, ema_fast):
    
    vhf_data = get_vhf_data(symbol, timeframe, ema_slow, ema_fast)
    fig = go.Figure(data=[go.Scatter(x=vhf_data.Time, y= vhf_data.VHF,
                  line={'color':'blue', 'width':1},     
                  mode='lines',
                  name='VHF'),
            ])

    fig.add_trace(go.Scatter(x=vhf_data.Time, y= vhf_data.VHF_EMA,
              line={'color':'red', 'width':1},
              #marker = 'o',
              mode='lines',
              name='VHF_EMA')
             )
    fig.update_xaxes(showgrid=False, showspikes=True, rangebreaks=[
                dict(bounds=["sat", "mon"]) #hide weekends
            ])
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', uirevision="Don't change")
    fig.update_layout(
            #height=800,
            showlegend=True,
            yaxis={'side': 'right'},
            #yaxis2 = False
            #title_text=f"Price & VFH({lookback})",
        )
    #fig.show()
    
    return fig


"""symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_D1
ema_slow = 200
ema_fast = 21

plot_subplots(symbol, timeframe, ema_slow, ema_fast)"""







