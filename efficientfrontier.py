from data import factor_returns, factor_tickers
import pandas as pd
import numpy as np


# Collect all prices into one dataframe
pre_prices = []
for ticker in factor_tickers:
    pre_prices.append(factor_returns[ticker][ticker])

# Drop nan to allow comparison of returns over same timeframe
daily_prices = pd.concat(pre_prices, axis=1).dropna()

# Log returns
log_ret = np.log(daily_prices).diff()

# Construct blank holders for returns, volatility, sharpe, and weights of randomised portfolios
np.random.seed(13)
num_ports = 10000
all_weights = np.zeros((num_ports, len(daily_prices.columns)))
rets_arr = np.zeros(num_ports)
vol_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for x in range(num_ports):
    # Generate random numbers in numpy array (between 1 and 0), then normalise to form random weights
    weights = np.array(np.random.random(len(daily_prices.columns)))
    weights = weights / np.sum(weights)

    # Save weights
    all_weights[x, :] = weights

    # Expected return as per hand written notes
    rets_arr[x] = np.sum((log_ret.mean() * weights * 252))

    # Expected volatility as per hand written notes
    vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))

    # Sharpe Ratio
    sharpe_arr[x] = rets_arr[x] / vol_arr[x]




