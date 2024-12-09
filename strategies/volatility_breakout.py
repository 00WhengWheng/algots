import pandas as pd
import numpy as np

from .indicators.volatility.bollinger_bands import bollinger_bands
from .indicators.volatility.average_true_range import average_true_range as atr
from .indicators.momentum.relative_strength_index import relative_strength_index as rsi

class VolatilityBreakout:
    def __init__(self, bb_period=20, bb_std=2, atr_period=14, rsi_period=14):
        super().__init__()
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.atr_period = atr_period
        self.rsi_period = rsi_period
        self.latest_volatility_value = None
        self.account_balance = 100000  # Initialize as needed
        self.risk_per_trade = 0.02  # 2% risk per trade
    required_patterns = ['bollinger_bands', 'atr', 'rsi']

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on Bollinger Bands, ATR, and RSI.

        :param data: Pandas DataFrame with price data.
        :return: DataFrame with signals.
        """
        # Calculate indicators
        data = bollinger_bands(data, period=self.bb_period, std=self.bb_std, column='Close')
        data = atr(data, period=self.atr_period)
        data['RSI'] = rsi(data['Close'], period=self.rsi_period)

        # Generate signals
        upper_col = f"Bollinger_Upper_{self.bb_period}"
        lower_col = f"Bollinger_Lower_{self.bb_period}"
        data['Signal'] = 0
        data['Position_Size'] = 0
        data['Stop_Loss'] = 0
        data['Take_Profit'] = 0

        for i in range(1, len(data)):
            if self._is_buy_signal(data.iloc[i-1], data.iloc[i]):
                data.loc[data.index[i], 'Signal'] = 1
                data.loc[data.index[i], 'Position_Size'] = self._calculate_position_size(data.iloc[i])
                data.loc[data.index[i], 'Stop_Loss'] = self._calculate_stop_loss(data.iloc[i], 'long')
                data.loc[data.index[i], 'Take_Profit'] = self._calculate_take_profit(data.iloc[i], 'long')
            elif self._is_sell_signal(data.iloc[i-1], data.iloc[i]):
                data.loc[data.index[i], 'Signal'] = -1
                data.loc[data.index[i], 'Position_Size'] = self._calculate_position_size(data.iloc[i])
                data.loc[data.index[i], 'Stop_Loss'] = self._calculate_stop_loss(data.iloc[i], 'short')
                data.loc[data.index[i], 'Take_Profit'] = self._calculate_take_profit(data.iloc[i], 'short')

        # Update latest volatility value
        self.latest_volatility_value = data[f'ATR_{self.atr_period}'].iloc[-1]
        return data

    def _is_buy_signal(self, prev, curr):
        return (
            curr['Close'] < curr[f"Bollinger_Lower_{self.bb_period}"] and
            curr['Close'] > prev['Close'] and
            curr['RSI'] < 30 and
            curr['Volume'] > prev['Volume'] * 1.2
        )

    def _is_sell_signal(self, prev, curr):
        return (
            curr['Close'] > curr[f"Bollinger_Upper_{self.bb_period}"] and
            curr['Close'] < prev['Close'] and
            curr['RSI'] > 70 and
            curr['Volume'] > prev['Volume'] * 1.2
        )

    def _calculate_position_size(self, row):
        risk_amount = self.account_balance * self.risk_per_trade
        return np.floor(risk_amount / row[f'ATR_{self.atr_period}'])

    def _calculate_stop_loss(self, row, direction):
        atr = row[f'ATR_{self.atr_period}']
        if direction == 'long':
            return row['Close'] - 2 * atr
        else:
            return row['Close'] + 2 * atr

    def _calculate_take_profit(self, row, direction):
        atr = row[f'ATR_{self.atr_period}']
        if direction == 'long':
            return row['Close'] + 3 * atr
        else:
            return row['Close'] - 3 * atr
    def check_position_size(self, account_balance, risk_per_trade):
        position_size = self._calculate_position_size({'Close': self.latest_volatility_value})
        max_position_size = account_balance * 0.05  # Maximum 5% of account balance
        return position_size <= max_position_size

    def check_daily_drawdown(self, daily_loss, max_drawdown=0.1):
        allowable_loss = max_drawdown * self.account_balance
        return daily_loss <= allowable_loss