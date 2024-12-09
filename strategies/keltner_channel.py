# strategies/KeltnerChannel.py

import pandas as pd

from .indicators.volatility.average_true_range import average_true_range as atr

class KeltnerChannel:
    # Define parameters
    parameters = {
        'atr_period': {
            'type': 'int',
            'default': 14,
            'description': 'ATR calculation period'
        },
        'multiplier': {
            'type': 'float',
            'default': 2.0,
            'description': 'Multiplier for ATR in Keltner Channels'
        },
        'risk_per_trade': {
            'type': 'float',
            'default': 0.01,
            'description': 'Fraction of account balance to risk per trade'
        },
        'max_drawdown': {
            'type': 'float',
            'default': 0.1,
            'description': 'Maximum allowed drawdown as a fraction of account balance'
        },
        'account_balance': {
            'type': 'float',
            'default': 100000.0,
            'description': 'Initial account balance'
        }
    }
    required_patterns = ['Triangle']

    def __init__(self, parameters):
        super().__init__(parameters)
        self.atr_period = int(parameters.get('atr_period', 14))
        self.multiplier = float(parameters.get('multiplier', 2.0))
        self.risk_per_trade = float(parameters.get('risk_per_trade', 0.01))
        self.max_drawdown = float(parameters.get('max_drawdown', 0.1))
        self.account_balance = float(parameters.get('account_balance', 100000.0))

    def calculate_position_size(self):
        position_size = self.risk_per_trade * self.account_balance
        return position_size

    def check_position_size(self, position_size):
        max_position_size = 0.02 * self.account_balance  # Limit to 2% of account balance
        return position_size <= max_position_size

    def check_daily_drawdown(self, daily_loss):
        allowable_loss = self.max_drawdown * self.account_balance
        return daily_loss <= allowable_loss

    def generate_signals(self, market_data):
        """
        Generate buy/sell signals using Keltner Channels and pattern detection.

        :param market_data: Dictionary containing market data.
        :return: List of signals.
        """
        data = market_data['data'].copy()
        symbol = market_data['symbol']
        datetime = market_data['datetime']

        # Ensure necessary columns are present
        required_columns = ['high', 'low', 'close']
        if not all(col in data.columns for col in required_columns):
            print("Error: Missing required price columns.")
            return []

        # Calculate ATR
        data = atr(data, period=self.atr_period, column_high='high', column_low='low', column_close='close')
        atr_col = f"ATR_{self.atr_period}"

        # Detect triangle patterns
        data = CandlestickPatterns.detect_triangle_pattern(data, column='close')

        # Calculate Keltner Channels
        data['Upper_Channel'] = data['close'] + (self.multiplier * data[atr_col])
        data['Lower_Channel'] = data['close'] - (self.multiplier * data[atr_col])

        # Generate signals based on Keltner Channels and patterns
        signals = []
        position_size = self.calculate_position_size()
        if not self.check_position_size(position_size):
            print("Position size exceeds risk limits.")
            return []

        # Check for sell signal
        if data['close'].iloc[-1] > data['Upper_Channel'].iloc[-1] and data['Triangle_Pattern'].iloc[-1]:
            signals.append({
                'type': 'SELL',
                'symbol': symbol,
                'datetime': datetime,
                'quantity': position_size
            })
        # Check for buy signal
        elif data['close'].iloc[-1] < data['Lower_Channel'].iloc[-1]:
            signals.append({
                'type': 'BUY',
                'symbol': symbol,
                'datetime': datetime,
                'quantity': position_size
            })

        return signals
