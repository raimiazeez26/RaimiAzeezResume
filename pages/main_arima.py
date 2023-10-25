# https://github.com/4QuantOSS/DashIntro/blob/master/notebooks/Tutorial.ipynb - plt to dash
#%matplotlib inline
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10, 6)  # Figure size and width

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from .def_symbols_tv import TIMEFRAME_DICT

def get_data(symbol, timeframe):
    df = pd.read_csv('forex_data.csv', index_col = [0])
    df = df.loc[(df['Symbol'] == symbol) & (df['TimeFrame'] == timeframe)]
    return df

def chart_data(symbol, timeframe, split=100, log = False, diff = False):

    #tf = TIMEFRAME_DICT[timeframe]
    df = get_data(symbol, timeframe)

    # Extract the 'Close' price
    data = df[['Close']]
    
    if log and diff:
        print('diff and log')
        data = np.log(data)
        data = data.diff().dropna()
    
        
    elif diff:
        print('diff')
        data = data.diff().dropna()
        
    elif log:
        print('log')
        data = np.log(data)

    split = split

    # Split the data into training and testing sets
    train_data = data.iloc[:-split]  # Using all but the last 10 days for training
    test_data = data.iloc[-split:]   # Last 10 days for testing

    fig, ax1 = plt.subplots(1,1, figsize=(10, 6))
    ax1.plot(train_data)
    ax1.set_title(f'{symbol} {timeframe} Chart')
    
    out_fig = fig_to_uri(fig)
    
    return train_data, test_data, out_fig

def acf_pcf(data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    plot_acf(data, lags=30, ax=ax1)
    plot_pacf(data, lags=30, ax=ax2)
    out_fig = fig_to_uri(fig)

    return out_fig

#https://stackoverflow.com/questions/65163961/displaying-model-summary-on-dash - dash display
def model_selection(data):
    # Perform auto ARIMA to determine the best model parameters
    model = auto_arima(data, seasonal=False, trace=True)

    # Get the best model parameters
    p, d, q = model.order

    # Print the best model parameters
    print(f"Best Model Parameters: p={p}, d={d}, q={q}")

    # Fit the ARIMA model
    model_fit = ARIMA(
        data, order=(p, d, q), trend="n"
    ).fit()
    #model_fit = model.fit(train_data, trend="n")

    # Model summary and diagnostics
    #print(model_fit.summary())
    
    return (p,d,q), model_fit, model_fit.summary()

def diagnostics(model):
    fig = model.plot_diagnostics(figsize=(10, 6))
    out_fig = fig_to_uri(fig)
    return out_fig

def forecast(model, train_data, test_data, symbol, timeframe, split=100, alpha1= 0.20, alpha2=0.05, ):
    # get forecast data for next 100 steps
    forecast = model.get_forecast(steps=split)
    forecast_mean = forecast.predicted_mean  # mean of forecast data
    conf_int95 = forecast.conf_int(alpha=alpha2)  # 95% confidence interval
    conf_int80 = forecast.conf_int(alpha=alpha1)  # 80% confidence interval
    
    fig, ax1 = plt.subplots(1,1, figsize=(10, 6))
    # plot mean forecast and 95% and 80% confidence intervals
    ax1.plot(train_data.reset_index(drop=True), label='Training Data')
    ax1.plot(forecast_mean.index, test_data.reset_index(drop=True), label='Actual Data')
    ax1.plot(forecast_mean, c="b", label='Forecast Mean')
    ax1.fill_between(
        conf_int95.index,
        conf_int95["lower Close"],
        conf_int95["upper Close"],
        color="b",
        alpha=0.3,
        label='95% Confidence Interval'
    )
    
    ax1.fill_between(
        conf_int80.index,
        conf_int80["lower Close"],
        conf_int80["upper Close"],
        color="b",
        alpha=0.5,
        label='80% Confidence Interval'
    )
    ax1.set_title(f'{symbol} {timeframe} Price Forecast')
    ax1.legend(loc = 'upper left')
    out_fig = fig_to_uri(fig)
    return out_fig

def forecast_log(model, train_data, test_data, symbol, timeframe, split=100, alpha1= 0.20, alpha2=0.05, ):
    # get forecast data for next 100 steps
    forecast = model.get_forecast(steps=split)
    forecast_mean = np.exp(forecast.predicted_mean)  # mean of forecast data
    conf_int95 = forecast.conf_int(alpha=alpha2)  # 95% confidence interval
    conf_int80 = forecast.conf_int(alpha=alpha1)  # 80% confidence interval
    
    fig, ax1 = plt.subplots(1,1, figsize=(10, 6))
    # plot mean forecast and 95% and 80% confidence intervals
    ax1.plot(np.exp(train_data.reset_index(drop=True)), label='Training Data')
    ax1.plot(forecast_mean.index, np.exp(test_data.reset_index(drop=True)), label='Actual Data')
    ax1.plot(forecast_mean, c="b", label='Forecast Mean')
    ax1.fill_between(
        conf_int95.index,
        np.exp(conf_int95["lower Close"]),
        np.exp(conf_int95["upper Close"]),
        color="b",
        alpha=0.3,
        label='95% Confidence Interval'
    )
    
    ax1.fill_between(
        conf_int80.index,
        np.exp(conf_int80["lower Close"]),
        np.exp(conf_int80["upper Close"]),
        color="b",
        alpha=0.5,
        label='80% Confidence Interval'
    )
    ax1.set_title(f'{symbol} {timeframe} Price Forecast')
    ax1.legend(loc = 'upper left')
    out_fig = fig_to_uri(fig)
    return out_fig


def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)