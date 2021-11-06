import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from config import factor_names


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


def eff_front_plot(mean, variance, weights, sharpe):
    return None


def correlation_plot(returns):
    renamed_ret = returns.set_axis(factor_names, axis=1, inplace=False)
    plt.figure(figsize=(10, 4))
    correlation_matrix = sns.heatmap(renamed_ret.corr(), vmin=-1, vmax=1, annot=True, cmap=cmap)
    # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
    correlation_matrix.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);
    plt.savefig('corrmatrix.png', dpi=300, bbox_inches='tight')
    return plt


def create_color(r, g, b):
    return [r / 256, g / 256, b / 256]
