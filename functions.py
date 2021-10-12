from config import *
import requests
import pandas as pd
import numpy as np


def get_histpri(ticker):
    # get response
    url = base_url + "historical-price-full/" + ticker + "?serietype=line&apikey=" + api_key
    response = requests.get(url)
    j = response.json()
    # clean response
    symbol = j['symbol']
    data = pd.DataFrame.from_dict(j['historical'])
    data.rename({'close': ticker}, axis=1, inplace=True)
    data.set_index('date', inplace=True)
    data.sort_index(ascending=True, inplace=True)
    return data


def cumulative_return(returns_df, column_name):
    returns_df['cum_ret'] = np.exp(np.log1p(returns_df[column_name]).cumsum())
    return returns_df


def get_attribute(dictionary, attribute):
    cr_list = []
    for factor in dictionary:
        if attribute == 'close_price':
            attribute = factor
            cr = dictionary[factor]
            cr.name = factor
            cr_list.append(cr)
        else:
            cr = dictionary[factor][attribute]
            cr.name = factor
            cr_list.append(cr)
    return pd.concat(cr_list, axis=1)


def check_sum(weights):
    # return 0 if sum of the weights is 1
    return np.sum(weights)-1

def get_ret_vol_sr(weights, returns):
    weights = np.array(weights)
    ret = np.sum(returns.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*252, weights)))
    sr = ret/vol
    return np.array([ret, vol, sr])

def neg_sharpe(weights):
# the number 2 is the sharpe ratio index from the get_ret_vol_sr
    return get_ret_vol_sr(weights)[2] * -1
