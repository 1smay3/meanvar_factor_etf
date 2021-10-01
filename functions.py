from config import *
import requests
import pandas as pd
import numpy as np

def get_histpri(ticker):
    # get reponse
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

def get_attribute(dictionary, attribtute):
    cr_list = []
    for factor in dictionary:
        cr = dictionary[factor][attribtute]
        cr.name = factor
        cr_list.append(cr)
    return pd.concat(cr_list, axis=1)