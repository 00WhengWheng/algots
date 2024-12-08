import pandas as pd
from ..utils.base_strategy import BaseStrategy
from ..patterns.trend_patterns import detect_double_top

class OrderFlowAnalysis(BaseStrategy):
    def __init__(self, buy_volume_col: str = 'Buy_Volume', sell_volume_col: str = 'Sell_Volume'):
        self.buy_volume_col = buy_volume_col
        self.sell_volume_col = sell_volume_col
    required_patterns = ['Double_Top']

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on order flow analysis and pattern detection.

        :param data: Pandas DataFrame with order flow data.
        :return: DataFrame with buy/sell signals.
        """
        if self.buy_volume_col not in data.columns or self.sell_volume_col not in data.columns:
            raise ValueError(f"Missing required columns: {self.buy_volume_col}, {self.sell_volume_col}")

        data['Order_Flow_Imbalance'] = data[self.buy_volume_col] - data[self.sell_volume_col]

        # Detect patterns
        data = detect_double_top(data, column='Close')

        # Generate signals
        data['Signal'] = 0
        data.loc[(data['Order_Flow_Imbalance'] > 0) & (data['Double_Top'] == False), 'Signal'] = 1  # Buy
        data.loc[(data['Order_Flow_Imbalance'] < 0), 'Signal'] = -1  # Sell

        return data