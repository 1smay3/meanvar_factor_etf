from config import factor_tickers
from database import read_daily_data
from efficientfrontier import efficient_frontier
from plotting import distribution_dashboard
import pandas as pd

# Collect all prices into one dataframe
pre_prices = []
for ticker in factor_tickers:
    factor_data = read_daily_data(ticker, "US")
    factor_prices = pd.Series(factor_data['adjClose'], name=ticker)
    rel_prices = factor_prices.to_frame()
    pre_prices.append(rel_prices)


# Drop nan to allow comparison of returns over same timeframe
daily_prices = pd.concat(pre_prices, axis=1).dropna()
daily_prices.to_excel("data_for_local_run.xlsx")

# plot distribution dashboard
distribution_dashboard(daily_prices.pct_change()).show()

weights, returns, volatility, sharpe = efficient_frontier(daily_prices)






