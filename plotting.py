from data import *
import pandas as pd
import matplotlib.pyplot as plt

cr_list = []
for factor in factor_returns:
    cr = factor_returns[factor]['cum_ret']
    cr.name=factor
    cr_list.append(cr)

pd.concat(cr_list, axis=1).plot()
plt.show()


# data_you_need=pd.DataFrame()
# for infile in glob.glob("*.xlsx"):
#     data = pandas.read_excel(infile)
#     data_you_need=data_you_need.append(data,ignore_index=True)