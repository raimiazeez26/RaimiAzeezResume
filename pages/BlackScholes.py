# Black-Scholes model in Python
import numpy as np
import pandas as pd
import scipy.stats as ss

def BS(S, K, r, vol, T, option_type):
  # dividend yield assumed to be 0

  # Compute d1 and d2
  d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
  d2 = d1 - vol * np.sqrt(T)

  if option_type in ["C", "P"]:
      if option_type in ["C"]:
          Opt_Price = S * ss.norm.cdf(d1) - K * np.exp(-r * T) * ss.norm.cdf(d2)
          Delta = ss.norm.cdf(d1)
          Gamma = ss.norm.pdf(d1) / (S * vol * np.sqrt(T))
          Vega = S * ss.norm.pdf(d1) * np.sqrt(T)
          Theta = -(S * ss.norm.pdf(d1) * vol) / (2 * np.sqrt(T)) - r * K * np.exp(
              -r * T
          ) * ss.norm.cdf(d2)
          Rho = K * T * np.exp(-r * T) * ss.norm.cdf(d2)
      else:
          Opt_Price = K * np.exp(-r * T) * ss.norm.cdf(-d2) - S * ss.norm.cdf(-d1)
          Delta = -ss.norm.cdf(-d1)
          Gamma = ss.norm.pdf(d1) / (S * vol * np.sqrt(T))
          Vega = S * ss.norm.pdf(d1) * np.sqrt(T)
          Theta = -(S * ss.norm.pdf(d1) * vol) / (2 * np.sqrt(T)) + r * K * np.exp(
              -r * T
          ) * ss.norm.cdf(-d2)
          Rho = -K * T * np.exp(-r * T) * ss.norm.cdf(-d2)
  else:
      Opt_Price = "Error: option type incorrect. Choose P for a put option or C for a call option."

  # print("Option price = {}".format(Opt_Price))
  # print("Delta = {}".format(Delta))
  # print("Gamma = {}".format(Gamma))
  # print("Vega = {}".format(Vega))
  # print("Theta = {}".format(Theta))
  # print("Rho = {}".format(Rho))

  return Opt_Price, Delta, Gamma, Vega, Theta, Rho

# T = 1.0  # supposed in years. It is not the maturity, but the time to maturity
# S = 12.5
# K = 15
# r = 0.01
# sigma = 0.45  # supposing it is annual
# opttype = "C"  # for the put insert 'P'

# data = BS(S, K, r, sigma, T, opttype)
# df = pd.DataFrame()
# df.index = ['Option price', 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho']
# df['value'] = list(data)
# print(df.round(2))

#print(BS(S, K, r, sigma, T, opttype))