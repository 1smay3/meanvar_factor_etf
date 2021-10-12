import seaborn as sns


def eff_front_plot(mean, variance, weights, sharpe):
    return None

def correlation_plot(returns):
    unstyle_corr = sns.heatmap(returns.corr())
    return unstyle_corr

