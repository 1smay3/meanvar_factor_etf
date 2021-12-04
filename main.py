import pandas as pd
from config import factor_tickers
from database import read_daily_data
from efficientfrontier import efficient_frontier
from plotting import distribution_dashboard, frontier_scatter

if __name__ == '__main__':

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

    # Plot distribution dashboard of chosen factors
    distribution_dashboard(daily_prices.pct_change())

    # Run mean_var optimisation
    mean_var_port = efficient_frontier.calculate(daily_prices, 10000)

    # Plot optimised portfolios
    frontier_scatter(mean_var_port, factor_tickers)
