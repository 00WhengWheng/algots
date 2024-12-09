import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import coint

class StatisticalArbitrage:
    def __init__(self, lookback_period: int = 60, z_score_threshold: float = 2.0):
        self.lookback_period = lookback_period
        self.z_score_threshold = z_score_threshold

    required_patterns = []
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals using statistical arbitrage.

        :param data: Pandas DataFrame with price data for multiple assets.
        :return: DataFrame with buy/sell signals.
        """
        if len(data.columns) < 2:
            raise ValueError("Statistical arbitrage requires at least two assets")

        # Calculate returns
        returns = data.pct_change().dropna()

        # Calculate spread
        spread = returns.iloc[:, 0] - returns.iloc[:, 1]

        # Calculate z-score
        z_score = (spread - spread.rolling(window=self.lookback_period).mean()) / spread.rolling(window=self.lookback_period).std()

        # Generate signals
        signals = pd.DataFrame(index=data.index, columns=data.columns)
        signals.iloc[:, 0] = np.where(z_score > self.z_score_threshold, -1, np.where(z_score < -self.z_score_threshold, 1, 0))
        signals.iloc[:, 1] = -signals.iloc[:, 0]  # Opposite signal for the second asset

        return signals

    def check_cointegration(self, data: pd.DataFrame) -> bool:
        """
        Check if the two assets are cointegrated.

        :param data: Pandas DataFrame with price data for two assets.
        :return: Boolean indicating whether the assets are cointegrated.
        """
        _, p_value, _ = coint(data.iloc[:, 0], data.iloc[:, 1])
        return p_value < 0.05  # Using 5% significance level