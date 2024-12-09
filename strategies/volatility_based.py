import pandas as pd
import numpy as np

from .indicators.volatility.bollinger_bands import bollinger_bands
from .indicators.volatility.average_true_range import average_true_range as atr
from .indicators.momentum.relative_strength_index import relative_strength_index as rsi

class VolatilityBased:
    def __init__(self, atr_period: int = 14, bb_period: int = 20, bb_std: float = 2.0, rsi_period: int = 14):
        self.atr_period = atr_period
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.rsi_period = rsi_period
        self.risk_per_trade = 0.02  # 2% risk per trade
    required_patterns = ['Flag', 'Triangle']

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals using enhanced volatility-based approach.

        :param data: Pandas DataFrame with price data.
        :return: DataFrame with buy/sell signals.
        """
        # Calculate indicators
        data = atr(data, period=self.atr_period, column_high='High', column_low='Low', column_close='Close')
        data = bollinger_bands(data, period=self.bb_period, std=self.bb_std, column='Close')
        data['RSI'] = rsi(data['Close'], period=self.rsi_period)

        # Detect patterns
        data = CandlestickPatterns.detect_flag_pattern(data, column='Close')
        data = CandlestickPatterns.detect_triangle_pattern(data, column='Close')

        # Generate signals
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

        return data

    def _is_buy_signal(self, prev, curr):
        return (
            curr['Close'] > curr['Upper_BB'] and
            curr['Close'] > prev['Close'] + prev[f'ATR_{self.atr_period}'] and
            curr['RSI'] < 70 and
            curr['Volume'] > prev['Volume'] * 1.5 and
            (curr['Flag_Pattern'] or curr['Triangle_Pattern'])
        )

    def _is_sell_signal(self, prev, curr):
        return (
            curr['Close'] < curr['Lower_BB'] and
            curr['Close'] < prev['Close'] - prev[f'ATR_{self.atr_period}'] and
            curr['RSI'] > 30 and
            curr['Volume'] > prev['Volume'] * 1.5 and
            (curr['Flag_Pattern'] or curr['Triangle_Pattern'])
        )

    def _calculate_position_size(self, row):
        account_balance = 100000  # Example account balance
        risk_amount = account_balance * self.risk_per_trade
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