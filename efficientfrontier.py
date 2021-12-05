from dataclasses import dataclass
import pandas as pd
import numpy as np
from tqdm import tqdm
from config import RANDOM_SEED, TD_PER_YEAR


@dataclass
class EfficientFrontier:
    all_weights: np.array
    all_weights_df: pd.DataFrame
    rets_arr: np.array
    rets_arr_df: pd.DataFrame
    vol_arr: np.array
    vol_arr_df: pd.DataFrame
    sharpe_arr: np.array
    sharpe_arr_df: pd.DataFrame

    def calculate(self: pd.DataFrame, iterations: int):
        # Log returns
        log_ret = np.log(self).diff()

        # Construct blank holders for returns, volatility, sharpe, and weights of randomised
        # portfolios

        np.random.seed(RANDOM_SEED)
        num_ports = iterations
        all_weights = np.zeros((num_ports, len(self.columns)))
        rets_arr = np.zeros(num_ports)
        vol_arr = np.zeros(num_ports)
        sharpe_arr = np.zeros(num_ports)

        print("\n")
        print("Running Optimisation with " + str(num_ports) + " iterations")
        for x in tqdm(range(num_ports)):

            # Generate random numbers in numpy array (between 1 and 0), then normalise to form random weights
            weights = np.array(np.random.random(len(self.columns)))
            weights = weights / np.sum(weights)

            # Save weights
            all_weights[x, :] = weights

            # Expected return as per hand written notes
            rets_arr[x] = np.sum((log_ret.mean() * weights * TD_PER_YEAR))

            # Expected volatility as per hand written notes
            vol_arr[x] = np.sqrt(
                np.dot(weights.T, np.dot(log_ret.cov() * TD_PER_YEAR, weights))
            )

            # Sharpe Ratio
            sharpe_arr[x] = rets_arr[x] / vol_arr[x]

        # Form df for easier manipulation and plotting
        all_weights_df = pd.DataFrame(all_weights, columns=self.columns)
        rets_arr_df = pd.DataFrame(rets_arr, columns=["returns"])
        vol_arr_df = pd.DataFrame(vol_arr, columns=["volatility"])
        sharpe_arr_df = pd.DataFrame(sharpe_arr, columns=["sharpe"])

        m_v_port = pd.concat(
            [all_weights_df, rets_arr_df, vol_arr_df, sharpe_arr_df], axis=1
        )
        print("Optimisation Complete")
        return m_v_port



