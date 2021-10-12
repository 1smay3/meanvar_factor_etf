
from data import factor_returns, factor_tickers
import pandas as pd
from functions import correlation_plot





# Collect all prices into one dataframe
pre_prices = []
for ticker in factor_tickers:
    pre_prices.append(factor_returns[ticker][ticker])

daily_prices = pd.concat(pre_prices, axis=1).dropna()
correlation_plot(daily_prices.pct_change()).show()


