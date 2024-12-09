from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self):
        self.position = None
        self.signals = []

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_position_size(self, data: pd.DataFrame) -> float:
        pass

    def backtest(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = self.generate_signals(data)
        return self._calculate_returns(signals, data)

    def _calculate_returns(self, signals: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        # Implement common return calculation logic here
        pass
