from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self):
        self.position = None
        self.signals = []
    
    @abstractmethod
    def generate_signals(self, data):
        pass
    
    @abstractmethod
    def calculate_position_size(self, data):
        pass
    
    def backtest(self, data):
        signals = self.generate_signals(data)
        return self._calculate_returns(signals, data)
