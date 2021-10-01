from data import factor_returns, factor_tickers
from functions import get_attribute

import numpy as np

daily_returns = get_attribute(factor_returns, 'daily_pct')
daily_returns.dropna(inplace=True)


#-- Get annualised mean returns
amr = (1+daily_returns.mean())**252 - 1
cov = daily_returns.cov()*252




# Efficient Frontier Simulations
n_assets = len(factor_tickers)
n_portfolios = 10000

# List to store mean_variance pairs
mean_variance_pairs = []

np.random.seed(75)

print("Generating Random Portfolios...")
# Generate random portfolios
for i in range(n_portfolios):
    # Choose assets randomly without replacement - not needed here as always including all
    assets = np.random.choice(list(daily_returns.columns), n_assets, replace=False)
    # Choose weights randomly
    weights = np.random.rand(n_assets)
    # - Ensure weights sum to 1
    weights = weights / sum(weights)

    # Loop over asset pairs and compute portfolio return and variance
    portfolio_E_Variance = 0
    portfolio_E_Return = 0
    for i in range(len(assets)):
        portfolio_E_Return += weights[i] * amr.loc[assets[i]]
        for j in range(len(assets)):
            # -- Add variance/covariance for each asset pair
            # - Note that when i==j this adds the variance
            portfolio_E_Variance += weights[i] * weights[j] * cov.loc[assets[i], assets[j]]

    mean_variance_pairs.append([portfolio_E_Return, portfolio_E_Variance])
