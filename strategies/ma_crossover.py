# src/strategies/ma_crossover.py

from .base_strategy import BaseStrategy
import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MACrossover(BaseStrategy):
    """Moving Average Crossover Strategy"""
    
    parameters = {
        'initial_capital': {
            'type': 'number',
            'default': 100000,
            'description': 'Initial Capital',
            'category': 'Account',
            'min': 1000,
            'max': 1000000
        },
        'risk_per_trade': {
            'type': 'number',
            'default': 0.02,
            'description': 'Risk Per Trade (%)',
            'category': 'Risk Management',
            'min': 0.01,
            'max': 0.05,
            'step': 0.01
        },
        'fast_ma_period': {
            'type': 'number',
            'default': 10,
            'description': 'Fast MA Period',
            'category': 'Indicator Settings',
            'min': 5,
            'max': 50
        },
        'slow_ma_period': {
            'type': 'number',
            'default': 20,
            'description': 'Slow MA Period',
            'category': 'Indicator Settings',
            'min': 10,
            'max': 100
        },
        'ma_type': {
            'type': 'select',
            'default': 'sma',
            'description': 'Moving Average Type',
            'category': 'Indicator Settings',
            'options': ['sma', 'ema', 'wma']
        }
    }

    def __init__(self, parameters: Dict[str, Any] = None):
        super().__init__(parameters)
        self.position = None

    def calculate_ma(self, data: pd.Series, period: int, ma_type: str = 'sma') -> pd.Series:
        if ma_type == 'ema':
            return data.ewm(span=period, adjust=False).mean()
        elif ma_type == 'wma':
            weights = np.arange(1, period + 1)
            return data.rolling(period).apply(
                lambda x: np.dot(x, weights) / weights.sum(), raw=True
            )
        else:  # sma
            return data.rolling(window=period).mean()

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        fast_ma = self.calculate_ma(
            data['Close'], 
            self.params['fast_ma_period'], 
            self.params['ma_type']
        )
        slow_ma = self.calculate_ma(
            data['Close'], 
            self.params['slow_ma_period'], 
            self.params['ma_type']
        )
        
        signals = pd.Series(0, index=data.index)
        signals[fast_ma > slow_ma] = 1
        signals[fast_ma < slow_ma] = -1
        
        return signals

    def calculate_position_size(self, price: float) -> float:
        return self.params['initial_capital'] * self.params['risk_per_trade'] / price
