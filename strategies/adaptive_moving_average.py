import pandas as pd
from ..utils.base_strategy import BaseStrategy
from ..patterns.trend_patterns import detect_head_and_shoulders
from ..indicators.trend import moving_average

class AdaptiveMovingAverage(BaseStrategy):
    # Define the parameters class variable
    parameters = {
        'short_period': {
            'type': 'int',
            'default': 10,
            'description': 'Short-term moving average period'
        },
        'long_period': {
            'type': 'int',
            'default': 50,
            'description': 'Long-term moving average period'
        }
    }
    required_patterns = ['Head_and_Shoulders_Pattern']

    def __init__(self, parameters):
        super().__init__(parameters)
        self.short_period = int(parameters.get('short_period', 10))
        self.long_period = int(parameters.get('long_period', 50))

    def generate_signals(self, market_data):
        """
        Generate buy/sell signals using adaptive moving averages and pattern detection.

        :param market_data: Dictionary containing market data for a symbol.
        :return: List of signals.
        """
        data = market_data['data'].copy()
        symbol = market_data['symbol']
        datetime = market_data['datetime']

        # Ensure the 'close' column is present
        if 'close' not in data:
            print("Error: 'close' column not found in data.")
            return []

        # Apply moving averages and pattern detection
        data = moving_average(data, period=self.short_period, column='close')
        data = moving_average(data, period=self.long_period, column='close')
        data = detect_head_and_shoulders(data, column='close')

        short_col = f"SMA_{self.short_period}"
        long_col = f"SMA_{self.long_period}"

        # Generate signals based on conditions
        signals = []
        if data[short_col].iloc[-1] > data[long_col].iloc[-1] and not data['Head_and_Shoulders_Pattern'].iloc[-1]:
            # Buy signal
            signals.append({
                'type': 'BUY',
                'symbol': symbol,
                'datetime': datetime,
                'quantity': 100  # You can adjust quantity as needed
            })
        elif data[short_col].iloc[-1] < data[long_col].iloc[-1]:
            # Sell signal
            signals.append({
                'type': 'SELL',
                'symbol': symbol,
                'datetime': datetime,
                'quantity': 100
            })

        return signals