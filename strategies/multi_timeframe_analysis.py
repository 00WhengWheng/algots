import pandas as pd
from ..utils.base_strategy import BaseStrategy
from ..indicators.trend import moving_average

class MultiTimeframeAnalysis(BaseStrategy):
    def __init__(self, short_period: int = 20, long_period: int = 50, timeframes: list = ["daily", "4h", "1h"]):
        self.short_period = short_period
        self.long_period = long_period
        self.timeframes = timeframes

    required_patterns = ['Triangle']

    def generate_signals(self, data: dict) -> pd.DataFrame:
        """
        Generate buy/sell signals using moving averages across multiple timeframes.

        :param data: Dictionary of Pandas DataFrames with price data for each timeframe.
        :return: DataFrame with buy/sell signals.
        """
        signals = {}
        for timeframe in self.timeframes:
            df = data[timeframe]
            df = moving_average(df, period=self.short_period, column='Close')
            df = moving_average(df, period=self.long_period, column='Close')

            short_col = f"SMA_{self.short_period}"
            long_col = f"SMA_{self.long_period}"

            df['Signal'] = 0
            df.loc[df[short_col] > df[long_col], 'Signal'] = 1  # Buy
            df.loc[df[short_col] < df[long_col], 'Signal'] = -1  # Sell

            signals[timeframe] = df['Signal']

        # Combine signals from different timeframes (you can implement your own logic here)
        final_signal = pd.DataFrame({tf: signals[tf] for tf in self.timeframes})
        final_signal['CombinedSignal'] = final_signal.sum(axis=1)

        return final_signal