
from io import BytesIO
import base64

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from arch import arch_model
from scipy import stats
from .def_symbols_tv import TIMEFRAME_DICT

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

def get_data(symbol, timeframe):
    df = pd.read_csv('forex_data.csv', index_col = [0])
    df = df.loc[(df['Symbol'] == symbol) & (df['TimeFrame'] == timeframe)]
    return df

def chart_data(symbol, timeframe, split=100, log = True, diff = True):

    #tf = TIMEFRAME_DICT[timeframe]
    df = get_data(symbol, timeframe)
    # Extract the 'Close' price
    data = df[['Close']]
    
    if log and diff:
        #print('diff and log')
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

def model_selection(train_data, p, q, dist = 'Normal'):
    
    # GARCH(1,1) Model with Normal White Noise
    garch_model = arch_model(
        train_data.Close,
        vol="GARCH",
        p=p,
        q=q,
        mean="AR",
        dist=dist, #StudentsT, Normal
        rescale=True,
    )
    model = garch_model.fit()
    summary = model.summary()
    return model, summary


def distribution(train_data, symbol, timeframe):

    # Histogram Histogram of Google Stock Returns
    fig, ax = plt.subplots(1,1, figsize=(10, 6))
    #plt.figure(figsize=(11, 5))
    goog_r = train_data.values

    x = np.linspace(min(goog_r), max(goog_r), len(goog_r))
    values, bins, _ = plt.hist(goog_r, bins=25)  # Histogram

    (mu, sigma) = stats.norm.fit(goog_r)
    ax.plot(x, stats.norm.pdf(x, mu, sigma) * sum(values * np.diff(bins)), "r")  # Density

    ax.set_title(f'{symbol} {timeframe} Distribution type')
    #plt.show()
    
    out_fig = fig_to_uri(fig)
    return out_fig

def diagnostics(train_data, garch_fit):

    # Model Diagnostic Plots ================================
    fig, ax = plt.subplots(4, 3, figsize=(10, 6))

    # Figure Row 1 Column 1
    ax[0, 0].plot(train_data)
    ax[0, 0].plot(2.0 * garch_fit.conditional_volatility / 100.0, c="r")
    ax[0, 0].plot(-2.0 * garch_fit.conditional_volatility / 100.0, c="r")
    ax[0, 0].tick_params(labelrotation=45)
    ax[0, 0].set_title("Series with 2 conditional SD")
    ax[0, 0].set_ylabel("Return")

    # Figure Row 1 Column 2
    VaR_1 = stats.t(df=len(train_data) - 1).ppf(0.99)
    # VaR_1 = stats.norm.ppf(0.99)
    ax[0, 1].plot(train_data)
    ax[0, 1].plot(VaR_1 * garch_fit.conditional_volatility / 100.0, c="r")
    ax[0, 1].plot(-VaR_1 * garch_fit.conditional_volatility / 100.0, c="r")
    ax[0, 1].tick_params(labelrotation=45)
    ax[0, 1].set_title("Series with 1% VaR Limits")
    ax[0, 1].set_ylabel("Return")

    # Figure Row 1 Column 3
    ax[0, 2].plot(garch_fit.conditional_volatility / 100.0)
    ax[0, 2].set_title("Conditional SD")
    ax[0, 2].tick_params(labelrotation=45)

    # Figure Row 2 Column 1
    sm.graphics.tsa.plot_acf(garch_fit.resid / 100.0, lags=20, ax=ax[1, 0])
    ax[1, 0].set_title("ACF of Observations")
    ax[1, 0].set_ylim([-0.3, 0.3])

    # Figure Row 2 Column 2
    sm.graphics.tsa.plot_acf(garch_fit.resid**2, lags=20, ax=ax[1, 1])
    ax[1, 1].set_title("ACF of Squared Observations")
    ax[1, 1].set_ylim([-0.3, 0.3])

    # Figure Row 2 Column 3
    sm.graphics.tsa.plot_acf(np.abs(garch_fit.resid), lags=20, ax=ax[1, 2])
    ax[1, 2].set_title("ACF of Absolute Observations")
    ax[1, 2].set_ylim([-0.3, 0.3])

    # Figure Row 3 Column 1
    ax[2, 0].xcorr(
        garch_fit.resid**2,
        garch_fit.resid,
        usevlines=True,
        maxlags=30,
        normed=True,
        lw=2,
    )
    ax[2, 0].set_title("Cross-Correlation of Squared Observations \n vs Actual Observation")

    # Figure Row 3 Column 2
    standaraized_residuals = garch_fit.std_resid
    min_val = np.min(standaraized_residuals)
    max_val = np.max(standaraized_residuals)
    empirical_density = np.linspace(min_val, max_val, len(standaraized_residuals))
    ax[2, 1].plot(empirical_density, stats.norm.pdf(empirical_density), lw=1)
    ax[2, 1].set_title("Empirical density of \n standarized residuals")

    # Figure Row 3 Column 3
    sm.qqplot(garch_fit.resid, stats.t, fit=True, line="q", ax=ax[2, 2])
    ax[2, 2].set_title("StudentsT QQ-plot")

    # Figure Row 4 Column 1
    sm.graphics.tsa.plot_acf(garch_fit.std_resid, lags=20, ax=ax[3, 0])
    ax[3, 0].set_title("ACF of Standarized Residuals")
    ax[3, 0].set_ylim([-0.12, 0.12])

    # Figure Row 4 Column 2
    sm.graphics.tsa.plot_acf((garch_fit.std_resid) ** 2, lags=20, ax=ax[3, 1])
    ax[3, 1].set_title("ACF of Squared Standarized Residuals")
    ax[3, 1].set_ylim([-0.12, 0.12])

    ax[3, 2].axis("off")
    fig.tight_layout()
    #plt.show()
    
    out_fig = fig_to_uri(fig)
    return out_fig

def forecast(model, train_data, test_data, symbol, timeframe, split):
    #Model Forecast
    # set horizon and forecast
    horizon = split
    garch_forecast = model.forecast(
        reindex=False, horizon=horizon, method="simulation"
    )

    # reindex data
    googr = train_data
    googr.index = list(range(len(train_data)))

    # forecast mean
    forc_mean = pd.Series(garch_forecast.mean.dropna().squeeze())
    forc_mean.index = list(range(len(googr), len(googr) + horizon))

    # volatility forecast
    variance_fct = pd.DataFrame(data={"Forecast": garch_forecast.variance.values[0]})
    variance_fct.index = list(range(len(googr), len(googr) + horizon))
    std_fct = [(variance_fct.values[i] * (i + 1)) ** 0.5 for i in range(len(variance_fct))]
    volatility_fct = pd.DataFrame(np.sqrt(std_fct))

    # upper/lower bands
    upper_band = googr.values[-1] * (1.0 + 2 * volatility_fct)
    upper_band.index = variance_fct.index
    lower_band = googr.values[-1] * (1.0 - 2 * volatility_fct)
    lower_band.index = variance_fct.index

    # Plot
    #plt.figure(figsize=(16, 7))
    fig, ax = plt.subplots(1,1, figsize=(10, 6))
    ax.plot(googr.index, googr, label='Train Data')
    ax.plot((upper_band + lower_band) / 2, "r--")
    ax.plot(forc_mean.index, test_data.Close, label='Test Data')
    ax.fill_between(
        upper_band.index.tolist(),
        upper_band.values.T[0],
        lower_band.values.T[0],
        color="orange",
        alpha=0.5,
    )
    ax.set_title(f'{symbol} {timeframe} Volatility Forecast')
    ax.legend(loc = 'upper left')
    #plt.show()
    
    out_fig = fig_to_uri(fig)
    return out_fig