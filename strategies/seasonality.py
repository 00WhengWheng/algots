import pandas as pd
from ..utils.base_strategy import BaseStrategy
from ..patterns.trend_patterns import detect_double_top

class Seasonality(BaseStrategy):
    def __init__(self, target_month: int):
        self.target_month = target_month
    required_patterns = ['Double_Top']

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on seasonality and pattern detection.

        :param data: Pandas DataFrame with price data.
        :return: DataFrame with buy/sell signals.
        """
        if 'Date' not in data.columns:
            raise ValueError("The 'Date' column is required to extract month data.")

        data['Month'] = pd.to_datetime(data['Date']).dt.month

        # Detect patterns
        data = detect_double_top(data, column='Close')

        # Generate signals based on seasonality and patterns
        data['Signal'] = 0
        data.loc[(data['Month'] == self.target_month) & (data['Double_Top'] == False), 'Signal'] = 1  # Buy
        data.loc[(data['Month'] != self.target_month), 'Signal'] = -1  # Sell

        return data