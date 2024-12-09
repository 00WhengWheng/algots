# strategies/DeltaNeutralHedging.py

import pandas as pd

from .patterns.technical.double_top import detect_double_top
from .indicators.utils import validate_data

class DeltaNeutralHedging:
    # Define the parameters class variable
    parameters = {
        'delta_threshold': {
            'type': 'float',
            'default': 0.5,
            'description': 'Threshold for delta hedging adjustments'
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
    required_patterns = ['DoubleTop']

    def __init__(self, parameters):
        super().__init__(parameters)
        self.delta_threshold = float(parameters.get('delta_threshold', 0.5))
        self.risk_per_trade = float(parameters.get('risk_per_trade', 0.01))
        self.max_drawdown = float(parameters.get('max_drawdown', 0.1))
        self.account_balance = float(parameters.get('account_balance', 100000.0))

    def calculate_position_size(self):
        """
        Calculate the position size based on the account balance and risk per trade.
        """
        position_size = self.risk_per_trade * self.account_balance
        return position_size

    def check_position_size(self, position_size):
        """
        Check if the calculated position size complies with risk management rules.
        """
        max_position_size = 0.02 * self.account_balance  # For example, limit to 2% of account balance
        return position_size <= max_position_size

    def check_daily_drawdown(self, daily_loss):
        """
        Ensure that the daily loss does not exceed the maximum allowable drawdown.
        """
        allowable_loss = self.max_drawdown * self.account_balance
        return daily_loss <= allowable_loss

    def generate_signals(self, market_data):
        """
        Generate hedge adjustment signals based on delta-neutral hedging strategy.

        :param market_data: Dictionary containing market data.
        :return: List of signals.
        """
        signals = []
        data = market_data['data'].copy()
        symbol = market_data['symbol']
        datetime = market_data['datetime']

        # Validate the input data
        if 'Delta' not in data.columns:
            print("Error: 'Delta' column not found in data.")
            return []

        # Identify where the absolute delta exceeds the threshold
        delta_value = data['Delta'].iloc[-1]
        if abs(delta_value) > self.delta_threshold:
            # Adjust the hedge by negating the delta
            position_size = self.calculate_position_size()

            # Check if position size is within limits
            if not self.check_position_size(position_size):
                print("Position size exceeds risk limits.")
                return []

            # Determine trade type
            if delta_value > 0:
                # Sell signal to reduce positive delta
                signals.append({
                    'type': 'SELL',
                    'symbol': symbol,
                    'datetime': datetime,
                    'quantity': position_size
                })
            else:
                # Buy signal to reduce negative delta
                signals.append({
                    'type': 'BUY',
                    'symbol': symbol,
                    'datetime': datetime,
                    'quantity': position_size
                })

        return signals
