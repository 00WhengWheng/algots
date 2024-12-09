from .indicators.volume.volume_weighted_average_price import calculate_vwap as vwap
from .patterns.technical.head_and_shoulders import head_and_shoulders
import pandas as pd
import numpy as np

from .base_strategy import BaseStrategy

from .indicators.volume.volume_weighted_average_price import calculate_vwap
from .patterns.technical.head_and_shoulders import head_and_shoulders

class VWAPTWAP(BaseStrategy):
    def __init__(self, vwap_period=20, twap_period=20, rsi_period=14, atr_period=14):
        super().__init__()
        self.account_balance = 100000  # Initialize as needed
        self.latest_close_price = None
        self.vwap_period = vwap_period
        self.twap_period = twap_period
        self.rsi_period = rsi_period
        self.atr_period = atr_period
    required_patterns = ['head_and_shoulders']

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on VWAP, TWAP, and head-and-shoulders pattern detection.
        """
        # Calculate VWAP
        data = vwap(data, column_close='Close', column_volume='Volume', window=self.vwap_period)

        # Calculate TWAP
        data['TWAP'] = data['Close'].rolling(window=self.twap_period).mean()

        # Calculate RSI
        delta = data['Close'].diff()


        # Calculate ATR
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        data['ATR'] = true_range.rolling(window=self.atr_period).mean()
        # Detect head-and-shoulders patterns
        data = detect_head_and_shoulders(data, column='Close')

        # Generate signals
        data['Signal'] = 0

        # Buy conditions
        buy_condition = (
            (data['Close'] > data['VWAP']) & 
            (data['Close'] > data['TWAP']) & 
            (data['RSI'] < 70) & 
            (~data['head_and_shoulders'])
        )
        data.loc[buy_condition, 'Signal'] = 1

        # Sell conditions
        sell_condition = (
            (data['Close'] < data['VWAP']) & 
            (data['Close'] < data['TWAP']) & 
            (data['RSI'] > 30)
        )
        data.loc[sell_condition, 'Signal'] = -1
        # Update latest close price
        self.latest_close_price = data['Close'].iloc[-1]

        data = calculate_vwap(data, column_close='Close', column_volume='Volume', window=self.vwap_period)
        data = detect_head_and_shoulders(data, column='Close')

        return data

    def calculate_position_size(self, account_balance, risk_per_trade):
        if self.latest_close_price is None or self.latest_atr is None:
            return 0

        risk_amount = account_balance * risk_per_trade
        position_size = risk_amount / (self.latest_atr * self.latest_close_price)
        return np.floor(position_size)
    def check_position_size(self, account_balance, risk_per_trade):
        position_size = self.calculate_position_size(account_balance, risk_per_trade)
        max_position_size = account_balance * 0.02 / self.latest_close_price
        return position_size <= max_position_size

    def check_daily_drawdown(self, daily_loss, max_drawdown=0.1):
        allowable_loss = max_drawdown * self.account_balance
        return daily_loss <= allowable_loss

    def update_strategy_state(self, data):
        self.latest_close_price = data['Close'].iloc[-1]
        self.latest_atr = data['ATR'].iloc[-1]