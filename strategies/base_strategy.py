from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, parameters: dict = None):
        self.parameters = parameters or {}

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_position_size(self, capital: float, current_bar: pd.Series) -> float:
        pass

    @abstractmethod
    def should_exit(self, position: dict, current_bar: pd.Series, signal_bar: pd.Series) -> float or None:
        pass

    @abstractmethod
    def calculate_stop_loss(self, bar: pd.Series, position_type: str) -> float:
        pass

    @abstractmethod
    def calculate_take_profit(self, bar: pd.Series, position_type: str) -> float:
        pass

    @abstractmethod
    def plot_strategy(self, data: pd.DataFrame, signals: pd.DataFrame, equity_curve: pd.Series):
        pass
