from .base_strategy import BaseStrategy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MACrossover(BaseStrategy):
    def __init__(self, fast_period: int = 10, slow_period: int = 30, initial_capital: float = 10000, risk_per_trade: float = 0.02):
        super().__init__(initial_capital, risk_per_trade)
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        data['fast_ma'] = data['Close'].rolling(window=self.fast_period).mean()
        data['slow_ma'] = data['Close'].rolling(window=self.slow_period).mean()

        data['Signal'] = np.where(data['fast_ma'] > data['slow_ma'], 1, 0)
        data['Signal'] = np.where(data['fast_ma'] < data['slow_ma'], -1, data['Signal'])

        return data

    def calculate_position_size(self, capital: float, current_price: float) -> float:
        # Calculate the position size based on the risk per trade
        risk_amount = capital * self.risk_per_trade
        stop_loss_percent = 0.02  # 2% stop loss
        shares = risk_amount / (current_price * stop_loss_percent)
        return round(shares)
    def calculate_stop_loss(self, entry_price: float, position: int) -> float:
        # Simple example: 2% stop loss
        return entry_price * (1 - 0.02 * position)

    def calculate_take_profit(self, entry_price: float, position: int) -> float:
        # Simple example: 4% take profit
        return entry_price * (1 + 0.04 * position)

    def should_exit(self, current_price: float, entry_price: float, position: int, stop_loss: float, take_profit: float) -> bool:
        if position > 0:
            return current_price <= stop_loss or current_price >= take_profit
        elif position < 0:
            return current_price >= stop_loss or current_price <= take_profit
        return False

    def plot_strategy(self, data: pd.DataFrame):
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.plot(data.index, data['fast_ma'], label=f'{self.fast_period} MA')
        plt.plot(data.index, data['slow_ma'], label=f'{self.slow_period} MA')

        plt.plot(data[data['Signal'] == 1].index, 
                 data['Close'][data['Signal'] == 1], 
                 '^', markersize=10, color='g', label='Buy Signal')

        plt.plot(data[data['Signal'] == -1].index, 
                 data['Close'][data['Signal'] == -1], 
                 'v', markersize=10, color='r', label='Sell Signal')

        plt.title('MA Crossover Strategy')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
