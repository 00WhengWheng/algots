from strategies.base_strategy import BaseStrategy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MovingAverageCrossover(BaseStrategy):
    def __init__(self, parameters: dict = None):
        super().__init__(parameters)
        self.short_window = self.parameters.get('short_window', 50)
        self.long_window = self.parameters.get('long_window', 200)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['Signal'] = 0.0

        # Create short and long moving averages
        signals['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        # Create signals
        signals['Signal'][self.short_window:] = np.where(signals['short_mavg'][self.short_window:] 
                                                         > signals['long_mavg'][self.short_window:], 1.0, 0.0)   
        signals['Signal'] = signals['Signal'].diff()

        return signals

    def calculate_position_size(self, capital: float, current_bar: pd.Series) -> float:
        return capital * 0.02 / current_bar['Close']  # 2% of capital

    def should_exit(self, position: dict, current_bar: pd.Series, signal_bar: pd.Series) -> float or None:
        if (position['type'] == 'long' and signal_bar['Signal'] == -1) or \
           (position['type'] == 'short' and signal_bar['Signal'] == 1):
            return current_bar['Close']
        return None

    def calculate_stop_loss(self, bar: pd.Series, position_type: str) -> float:
        return bar['Close'] * 0.95 if position_type == 'long' else bar['Close'] * 1.05

    def calculate_take_profit(self, bar: pd.Series, position_type: str) -> float:
        return bar['Close'] * 1.1 if position_type == 'long' else bar['Close'] * 0.9

    def plot_strategy(self, data: pd.DataFrame, signals: pd.DataFrame, equity_curve: pd.Series):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        ax1.plot(data.index, data['Close'], label='Close Price')
        ax1.plot(signals.index, signals['short_mavg'], label=f'{self.short_window} MA')
        ax1.plot(signals.index, signals['long_mavg'], label=f'{self.long_window} MA')
        ax1.scatter(signals.index[signals['Signal'] == 1], data['Close'][signals['Signal'] == 1], 
                    label='Buy Signal', marker='^', color='g')
        ax1.scatter(signals.index[signals['Signal'] == -1], data['Close'][signals['Signal'] == -1], 
                    label='Sell Signal', marker='v', color='r')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.set_title('Moving Average Crossover Strategy')

        ax2.plot(equity_curve.index, equity_curve, label='Equity Curve')
        ax2.set_ylabel('Portfolio Value')
        ax2.set_xlabel('Date')
        ax2.legend()

        plt.tight_layout()
        return fig
