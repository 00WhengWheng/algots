import pandas as pd
import numpy as np
from ..utils.base_strategy import BaseStrategy
from ..indicators.momentum import rsi, stochastic_oscillator
from ..indicators.trend import MovingAverage
from ..patterns.candlestick import CandlestickPatterns

class MomentumTrading(BaseStrategy):
    def __init__(self, rsi_period: int = 14, stochastic_period: int = 14, ma_period: int = 50):
        self.rsi_period = rsi_period
        self.stochastic_period = stochastic_period
        self.ma_period = ma_period
        self.stop_loss_pct = 0.02  # 2% stop loss
        self.take_profit_pct = 0.04  # 4% take profit
        self.max_holding_days = 5  # Maximum holding period

    required_patterns = ['Doji', 'Hammer']
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals using RSI, Stochastic Oscillator, Moving Average, and candlestick patterns.

        :param data: Pandas DataFrame with price data.
        :return: DataFrame with buy/sell signals.
        """
        # Calculate indicators
        data = rsi(data, period=self.rsi_period, column='Close')
        data = stochastic_oscillator(data, period=self.stochastic_period)
        data = MovingAverage.sma(data, period=self.ma_period, column='Close')

        # Detect candlestick patterns
        data = CandlestickPatterns.detect_hammer(data, high_col='High', low_col='Low', close_col='Close')
        data = CandlestickPatterns.detect_doji(data, open_col='Open', close_col='Close')

        # Calculate volume moving average
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        # Generate signals based on indicators and patterns
        data['Signal'] = 0
        data.loc[(data[f"RSI_{self.rsi_period}"] < 30) & 
                 (data['%K_14'] < 20) & 
                 (data['Hammer'] == True) & 
                 (data['Close'] > data[f'SMA_{self.ma_period}']) &
                 (data['Volume'] > data['Volume_MA']), 'Signal'] = 1  # Buy

        data.loc[(data[f"RSI_{self.rsi_period}"] > 70) & 
                 (data['%K_14'] > 80) & 
                 (data['Doji'] == True) & 
                 (data['Close'] < data[f'SMA_{self.ma_period}']) &
                 (data['Volume'] > data['Volume_MA']), 'Signal'] = -1  # Sell

        # Apply stop loss and take profit
        data = self.apply_stop_loss_take_profit(data)

        # Apply time-based exit
        data = self.apply_time_based_exit(data)

        return data

    def apply_stop_loss_take_profit(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply stop loss and take profit to the signals.
        """
        position = 0
        entry_price = 0
        for i in range(len(data)):
            if data['Signal'].iloc[i] == 1 and position == 0:
                position = 1
                entry_price = data['Close'].iloc[i]
            elif data['Signal'].iloc[i] == -1 and position == 0:
                position = -1
                entry_price = data['Close'].iloc[i]
            elif position != 0:
                current_price = data['Close'].iloc[i]
                if position == 1:
                    if current_price <= entry_price * (1 - self.stop_loss_pct) or current_price >= entry_price * (1 + self.take_profit_pct):
                        data.loc[data.index[i], 'Signal'] = -1
                        position = 0
                elif position == -1:
                    if current_price >= entry_price * (1 + self.stop_loss_pct) or current_price <= entry_price * (1 - self.take_profit_pct):
                        data.loc[data.index[i], 'Signal'] = 1
                        position = 0
        return data

    def apply_time_based_exit(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply time-based exit to the signals.
        """
        position = 0
        entry_time = None
        for i in range(len(data)):
            if data['Signal'].iloc[i] != 0 and position == 0:
                position = data['Signal'].iloc[i]
                entry_time = data.index[i]
            elif position != 0:
                current_time = data.index[i]
                if (current_time - entry_time).days >= self.max_holding_days:
                    data.loc[data.index[i], 'Signal'] = -position
                    position = 0
        return data