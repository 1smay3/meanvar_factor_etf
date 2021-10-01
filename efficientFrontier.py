from data import factor_returns, factor_tickers
from functions import get_attribute

import numpy as np

daily_returns = get_attribute(factor_returns, 'daily_pct')

#-- Get annualised mean returns
amr = (1+daily_returns.mean())**252 - 1
cov = daily_returns.cov()*252

print("Debug")


# Efficient Frontier Simulations
n_assets = len(factor_tickers)
n_portfolios = 1000

# List to store mean_variance pairs
mean_variance_pairs = []

np.random.seed(75)
# Generate random portfolios
for i in range(n_portfolios):