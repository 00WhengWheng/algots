import pandas as pd
from ..utils.base_strategy import BaseStrategy
from ..indicators.momentum import rsi
from ..utils.technical_indicators import TechnicalIndicators
from ..patterns.candlestick import CandlestickPatterns

class MeanReversion(BaseStrategy):
    parameters = {
        'rsi_period': {
            'type': 'int',
            'default': 14,
            'description': 'Period for RSI calculation'
        },
        'rsi_oversold': {
            'type': 'int',
            'default': 30,
            'description': 'RSI level considered oversold'
        },
        'rsi_overbought': {
            'type': 'int',
            'default': 70,
            'description': 'RSI level considered overbought'
        },
        'volume_factor': {
            'type': 'float',
            'default': 1.5,
            'description': 'Factor to compare current volume with average'
        },
        'stop_loss': {
            'type': 'float',
            'default': 0.02,
            'description': 'Stop loss percentage'
        },
        'take_profit': {
            'type': 'float',
            'default': 0.03,
            'description': 'Take profit percentage'
        }
    }
    required_patterns = ['Doji']

    def __init__(self, parameters):
        super().__init__(parameters)
        self.rsi_period = int(parameters.get('rsi_period', 14))
        self.rsi_oversold = int(parameters.get('rsi_oversold', 30))
        self.rsi_overbought = int(parameters.get('rsi_overbought', 70))
        self.volume_factor = float(parameters.get('volume_factor', 1.5))
        self.stop_loss = float(parameters.get('stop_loss', 0.02))
        self.take_profit = float(parameters.get('take_profit', 0.03))

    def generate_signals(self, market_data):
        """
        Generate buy/sell signals using RSI, Doji pattern detection, and volume confirmation.
        """
        data = market_data['data'].copy()
        symbol = market_data['symbol']
        datetime = market_data['datetime']

        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required_columns):
            print("Error: Missing required price columns.")
            return []

        # Calculate RSI
        data = TechnicalIndicators.rsi(data, period=self.rsi_period, column='close')
        rsi_col = f"RSI_{self.rsi_period}"

        # Detect Doji patterns
        data = CandlestickPatterns.detect_doji(data, open_col='open', close_col='close')

        # Calculate average volume
        data['avg_volume'] = data['volume'].rolling(window=20).mean()
        signals = []
        last_close = data['close'].iloc[-1]

        if (data[rsi_col].iloc[-1] < self.rsi_oversold and 
            data['Doji'].iloc[-1] and 
            data['volume'].iloc[-1] > self.volume_factor * data['avg_volume'].iloc[-1]):
            # Buy signal
            signals.append({
                'type': 'BUY',
                'symbol': symbol,
                'datetime': datetime,
                'price': last_close,
                'quantity': 100,  # Adjust quantity as needed
                'stop_loss': last_close * (1 - self.stop_loss),
                'take_profit': last_close * (1 + self.take_profit)
            })
        elif data[rsi_col].iloc[-1] > self.rsi_overbought:
            # Sell signal
            signals.append({
                'type': 'SELL',
                'symbol': symbol,
                'datetime': datetime,
                'price': last_close,
                'quantity': 100
            })

        return signals

    def update_stops(self, position, current_price):
        """
        Update stop loss and take profit levels for an open position.
        """
        if position['type'] == 'BUY':
            new_stop_loss = max(position['stop_loss'], current_price * (1 - self.stop_loss))
            new_take_profit = max(position['take_profit'], current_price * (1 + self.take_profit))
            return new_stop_loss, new_take_profit
        return position['stop_loss'], position['take_profit']
