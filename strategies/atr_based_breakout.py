# src/strategies/atr_based_breakout.py

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ATRBasedBreakout(BaseStrategy):
    """ATR-Based Breakout Trading Strategy"""
    
    parameters = {
        'initial_capital': {
            'type': 'number',
            'default': 100000,
            'description': 'Initial Capital',
            'category': 'Account',
            'min': 1000,
            'max': 1000000
        },
        # ... rest of the parameters ...
    }

    def __init__(self, parameters: Dict[str, Any] = None):
        super().__init__(parameters)
        self.position = None
        self.stop_loss = None

    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        atr = self.calculate_atr(data, self.params['atr_period'])
        
        upper_band = data['High'].rolling(window=self.params['atr_period']).max() + \
                    atr * self.params['atr_multiplier']
        lower_band = data['Low'].rolling(window=self.params['atr_period']).min() - \
                    atr * self.params['atr_multiplier']
        
        signals = pd.Series(0, index=data.index)
        
        for i in range(self.params['atr_period'], len(data)):
            if data['Close'].iloc[i] > upper_band.iloc[i-1]:
                signals.iloc[i] = 1
            elif data['Close'].iloc[i] < lower_band.iloc[i-1]:
                signals.iloc[i] = -1
            
            if self.params['use_stop_loss'] and self.position is not None:
                if self.position > 0 and data['Low'].iloc[i] < self.stop_loss:
                    signals.iloc[i] = -1
                elif self.position < 0 and data['High'].iloc[i] > self.stop_loss:
                    signals.iloc[i] = 1
        
        return signals

    def calculate_position_size(self, price: float) -> float:
        if self.params['position_size_type'] == 'risk_based':
            risk_amount = self.params['initial_capital'] * self.params['risk_per_trade']
            atr_stop = price * self.params['atr_multiplier']
            return risk_amount / atr_stop
        else:
            return self.params['initial_capital'] * self.params['risk_per_trade'] / price

    def update_position(self, signal: int, price: float) -> None:
        if signal != 0:
            self.position = signal
            if self.params['use_stop_loss']:
                stop_distance = price * self.params['atr_multiplier']
                self.stop_loss = price - (signal * stop_distance)
