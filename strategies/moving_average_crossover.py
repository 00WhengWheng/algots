# src/strategies/moving_average_crossover.py

import pandas as pd
import numpy as np
from src.indicators.trend import MovingAverage

class MovingAverageCrossover:
    """
    Moving Average Crossover strategy implementation.
    """
    
    parameters = {
        'fast_ma_period': {
            'type': 'number',
            'default': 20,
            'description': 'Fast Moving Average Period',
            'category': 'Indicator Settings',
            'min': 1,
            'max': 200,
            'step': 1
        },
        'slow_ma_period': {
            'type': 'number',
            'default': 50,
            'description': 'Slow Moving Average Period',
            'category': 'Indicator Settings',
            'min': 1,
            'max': 200,
            'step': 1
        },
        'ma_type': {
            'type': 'select',
            'default': 'sma',
            'description': 'Moving Average Type',
            'category': 'Indicator Settings',
            'options': ['sma', 'ema', 'wma']
        },
        'position_size': {
            'type': 'number',
            'default': 1.0,
            'description': 'Position Size (as fraction of capital)',
            'category': 'Risk Management',
            'min': 0.1,
            'max': 1.0,
            'step': 0.1
        },
        'stop_loss': {
            'type': 'number',
            'default': 0.02,
            'description': 'Stop Loss (as fraction)',
            'category': 'Risk Management',
            'min': 0.01,
            'max': 0.1,
            'step': 0.01
        },
        'take_profit': {
            'type': 'number',
            'default': 0.04,
            'description': 'Take Profit (as fraction)',
            'category': 'Risk Management',
            'min': 0.01,
            'max': 0.2,
            'step': 0.01
        }
    }

    def __init__(self, parameters=None):
        """Initialize strategy with parameters."""
        self.params = parameters or {}
        for param, config in self.parameters.items():
            if param not in self.params:
                self.params[param] = config['default']
        
        self.ma_calculator = MovingAverage()

    def generate_signals(self, market_data):
        """
        Generate trading signals based on moving average crossover.
        
        Args:
            market_data (pd.DataFrame): Market data with OHLCV
            
        Returns:
            pd.Series: Trading signals (1 for buy, -1 for sell, 0 for hold)
        """
        # Set the data for MovingAverage calculator
        self.ma_calculator.data = market_data['Close']
        
        # Calculate fast and slow moving averages
        if self.params['ma_type'] == 'ema':
            fast_ma = self.ma_calculator.ema(self.params['fast_ma_period'])
            slow_ma = self.ma_calculator.ema(self.params['slow_ma_period'])
        elif self.params['ma_type'] == 'wma':
            fast_ma = self.ma_calculator.wma(self.params['fast_ma_period'])
            slow_ma = self.ma_calculator.wma(self.params['slow_ma_period'])
        else:  # default to SMA
            fast_ma = self.ma_calculator.sma(self.params['fast_ma_period'])
            slow_ma = self.ma_calculator.sma(self.params['slow_ma_period'])
        
        # Generate signals
        signals = pd.Series(0, index=market_data.index)
        signals[fast_ma > slow_ma] = 1  # Buy signal
        signals[fast_ma < slow_ma] = -1  # Sell signal
        
        return signals

    def calculate_position_size(self, capital):
        """Calculate position size based on parameters."""
        return capital * self.params['position_size']
