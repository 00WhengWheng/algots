from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, initial_capital: float, risk_per_trade: float):
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_position_size(self, capital: float, current_price: float) -> float:
        pass

    @abstractmethod
    def calculate_stop_loss(self, entry_price: float, position: int) -> float:
        pass

    @abstractmethod
    def calculate_take_profit(self, entry_price: float, position: int) -> float:
        pass

    @abstractmethod
    def should_exit(self, current_price: float, entry_price: float, position: int, stop_loss: float, take_profit: float) -> bool:
        pass

    @abstractmethod
    def plot_strategy(self, data: pd.DataFrame):
        pass
