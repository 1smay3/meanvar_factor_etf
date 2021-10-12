import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

api_key = "6a7bfe0b2162048feb12ab86dbd15631"
version = "v3"
base_url = "https://financialmodelingprep.com/api/" + version + "/"


factor_names = ['Value', 'Growth', 'Momentum', 'Small-Cap', 'Dividend Yield', 'Low-Vol']

# Create linear custom colour maps for correlation matrices
# TODO: Move somewhere better and have factor tickers mapped to them? Or is that bad design
np.random.seed(13)
sns.set()

def create_color(r, g, b):
    return [r / 256, g / 256, b / 256]


def get_custom_color_palette():
    return LinearSegmentedColormap.from_list("", [
        create_color(0,245,142), create_color(255, 255, 255)
    ])


low, high = -1, 1
data = np.random.uniform(low, high, (10, 15))
cmap = get_custom_color_palette()
