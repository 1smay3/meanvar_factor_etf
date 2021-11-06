from arctic import Arctic
from config import factor_tickers

# Connect to Local MONGODB
store = Arctic('localhost')
# Access the library
library = store['FACTORS']


# Reading the data
item = library.read('IWD')
factor = item.data
metadata = item.metadata

print(factor)