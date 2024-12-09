import pandas as pd
import numpy as np

from .indicators.trend.moving_average import moving_average
from .patterns.technical.head_and_shoulders import head_and_shoulders
from .patterns.technical.double_top import detect_double_top

class TrendFollowing:
    def __init__(self, short_period: int = 20, long_period: int = 50, atr_period: int = 14):
        self.short_period = short_period
        self.long_period = long_period
        self.atr_period = atr_period

    required_patterns = ['Head_and_Shoulders_Pattern', 'Double_Top']
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals using trend following techniques.

        :param data: Pandas DataFrame with price data.
        :return: DataFrame with buy/sell signals.
        """
        # Calculate moving averages
        data = moving_average(data, period=self.short_period, column='Close')
        data = moving_average(data, period=self.long_period, column='Close')

        # Calculate ATR for volatility-based position sizing
        data['ATR'] = self.calculate_atr(data, self.atr_period)
        # Detect patterns
        data = detect_head_and_shoulders(data, column='Close')
        data = detect_double_top(data, column='Close')

        short_col = f"SMA_{self.short_period}"
        long_col = f"SMA_{self.long_period}"

        # Generate signals based on moving averages and patterns
        data['Signal'] = 0
        data.loc[(data[short_col] > data[long_col]) & 
                 (data['Head_and_Shoulders_Pattern'] == False) & 
                 (data['Double_Top'] == False), 'Signal'] = 1  # Buy signal

        data.loc[(data[short_col] < data[long_col]) | 
                 (data['Head_and_Shoulders_Pattern'] == True) | 
                 (data['Double_Top'] == True), 'Signal'] = -1  # Sell signal

        # Calculate position size based on ATR
        data['Position_Size'] = self.calculate_position_size(data)

        return data

    def calculate_atr(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

    def calculate_position_size(self, data: pd.DataFrame) -> pd.Series:
        """Calculate position size based on ATR"""
        risk_per_trade = 0.01  # 1% risk per trade
        account_balance = 100000  # Example account balance
        risk_amount = account_balance * risk_per_trade
        return (risk_amount / data['ATR']).round()