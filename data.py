from functions import get_histpri, cumulative_return


factor_tickers = ['IWD', 'IWF', 'MTUM', 'IJR', 'VYM', 'USMV']


factor_returns ={}
for ticker in factor_tickers:
    price_data = get_histpri(ticker)
    # add daily return
    price_data['daily_pct'] = price_data.pct_change()
    cum_ret = cumulative_return(price_data, 'daily_pct')
    # add cleaned returns to dictionary
    factor_returns[ticker] = cum_ret



