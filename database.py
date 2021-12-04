# Process and standardise data to be used across other files
from config import *
import requests
import pandas as pd
from arctic import Arctic

store = Arctic("localhost")


def new_data(ticker, database):
    # get response
    url = (
        base_url
        + "historical-price-full/"
        + ticker
        + "?serietype=line&apikey="
        + api_key
    )
    response = requests.get(url)
    j = response.json()
    # clean response
    data = pd.DataFrame.from_dict(j["historical"])
    data.rename({"close": ticker}, axis=1, inplace=True)
    data.set_index("date", inplace=True)
    data.sort_index(ascending=True, inplace=True)
    # store data
    library = store[database]
    library.write(ticker, data, metadata={"source": "Financial Modelling Prep"})
    return None


def read_daily_data(ticker, database):
    db_ticker = ticker + "_EOD"
    library = store[database]
    library_obj = library.read(db_ticker)
    return library_obj.data
