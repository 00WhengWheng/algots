import pandas as pd
from ..utils.base_strategy import BaseStrategy

class EventDriven(BaseStrategy):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.event_column = parameters.get('event_column', 'Event')
        self.sma_period = int(parameters.get('sma_period', 20))
        self.ema_period = int(parameters.get('ema_period', 50))
        self.risk_per_trade = float(parameters.get('risk_per_trade', 0.01))

    parameters = {
        'event_column': {
            'type': 'text',
            'default': 'Event',
            'description': 'Name of the column containing event data'
        },
        'sma_period': {
            'type': 'int',
            'default': 20,
            'description': 'Simple Moving Average period'
        },
        'ema_period': {
            'type': 'int',
            'default': 50,
            'description': 'Exponential Moving Average period'
        },
        'risk_per_trade': {
            'type': 'float',
            'default': 0.01,
            'description': 'Percentage of account balance to risk per trade'
        }
    }
    required_patterns = []

    def generate_signals(self, market_data):
        """
        Generate buy/sell signals based on specific events and technical indicators.

        :param market_data: Dictionary containing market data.
        :return: List of signals.
        """
        data = market_data['data']
        symbol = market_data['symbol']
        datetime = market_data['datetime']

        if self.event_column not in data.columns:
            print(f"Error: Missing required event column: {self.event_column}")
            return []

        # Calculate SMA and EMA
        data['SMA'] = data['Close'].rolling(window=self.sma_period).mean()
        data['EMA'] = data['Close'].ewm(span=self.ema_period, adjust=False).mean()

        # Get the latest data point
        latest_data = data.iloc[-1]
        event_value = latest_data[self.event_column]
        sma_value = latest_data['SMA']
        ema_value = latest_data['EMA']
        close_price = latest_data['Close']

        signals = []

        # Calculate position size based on risk
        account_balance = self.get_account_balance()  # Implement this method in BaseStrategy
        risk_amount = account_balance * self.risk_per_trade
        position_size = int(risk_amount / close_price)

        # Generate BUY signal
        if (event_value == 'BUY' and 
            close_price > sma_value and 
            close_price > ema_value and 
            data['Volume'].iloc[-1] > data['Volume'].rolling(window=20).mean().iloc[-1]):
            signals.append({
                'type': 'BUY',
                'symbol': symbol,
                'datetime': datetime,
                'quantity': position_size
            })

        # Generate SELL signal
        elif (event_value == 'SELL' and 
              close_price < sma_value and 
              close_price < ema_value and 
              data['Volume'].iloc[-1] > data['Volume'].rolling(window=20).mean().iloc[-1]):
            signals.append({
                'type': 'SELL',
                'symbol': symbol,
                'datetime': datetime,
                'quantity': position_size
            })

        return signals

    def get_account_balance(self):
        # Implement this method to fetch the current account balance
        # This could involve querying a database or an API
        # For now, we'll return a dummy value
        return 100000.0
