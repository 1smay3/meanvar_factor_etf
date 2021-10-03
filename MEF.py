from functions import get_attribute
from data import factor_returns, factor_tickers
from functions import check_sum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Get all prices in one df

#daily_price = get_attribute(factor_returns, 'close_price')

test = factor_returns
pre_prices = []
for ticker in factor_tickers:
    pre_prices.append(factor_returns[ticker][ticker])

daily_prices = pd.concat(pre_prices, axis=1).dropna()

log_ret = np.log(daily_prices/daily_prices.shift(1))

np.random.seed(13)
num_ports = 10000
all_weights = np.zeros((num_ports, len(daily_prices.columns)))
ret_arr = np.zeros(num_ports)
vol_arr = np.zeros(num_ports)
sharpe_arr = np.zeros(num_ports)

for x in range(num_ports):
    # Weights
    weights = np.array(np.random.random(len(daily_prices.columns)))
    weights = weights / np.sum(weights)

    # Save weights
    all_weights[x, :] = weights

    # Expected return
    ret_arr[x] = np.sum((log_ret.mean() * weights * 252))

    # Expected volatility
    vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))

    # Sharpe Ratio
    sharpe_arr[x] = ret_arr[x] / vol_arr[x]

def get_ret_vol_sr(weights):
    weights = np.array(weights)
    ret = np.sum(log_ret.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
    sr = ret/vol
    return np.array([ret, vol, sr])

def neg_sharpe(weights):
# the number 2 is the sharpe ratio index from the get_ret_vol_sr
    return get_ret_vol_sr(weights)[2] * -1



# Optimisation
# Set Constraints
cons = ({'type':'eq', 'fun': check_sum})
# Set bounds of inital optimisation guess - weights between 0 and 1
# TODO this is horrible code (change from tuple) - change so its not tuples, or change so it varies wiht how many assets you choose
bounds=((0,1),(0,1),(0,1),(0,1),(0,1),(0,1))
b_g = 1/7
initial_guess = [b_g,b_g,b_g,b_g,b_g,b_g]

optim_out = minimize(neg_sharpe, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)

# get ret, vol, sr of the optimal portfolio
print(get_ret_vol_sr(optim_out.x))

# Build efficient frontier line
frontier_y = np.linspace(0.075,0.15, 200)

def minimize_volatility(weights):
    return get_ret_vol_sr(weights)[1]


frontier_x = []

#this is mad slow
for possible_return in frontier_y:
    cons = ({'type': 'eq', 'fun': check_sum},
            {'type': 'eq', 'fun': lambda w: get_ret_vol_sr(w)[0] - possible_return})

    result = minimize(minimize_volatility, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)
    frontier_x.append(result['fun'])

# change to plotly and have weights built in
plt.figure(figsize=(12,8))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.plot(frontier_x,frontier_y, 'r--', linewidth=3)

plt.show()