import asyncio
from typing import Dict, Any
import pandas as pd
from .backtest import Backtester
from strategies.strategy_loader import StrategyLoader
from data.data_fetcher import DataFetcher
import logging
import requests

class BacktestingApp:
    def __init__(self):
        self.backtester = Backtester()
        self.strategy_loader = StrategyLoader()
        self.data_fetcher = DataFetcher()
        self.logger = logging.getLogger(__name__)

    def run_backtest(self, strategy_name: str, symbol: str, start_date: str, end_date: str, params: dict = None):
        try:
            # Fetch data using yfinance
            data = self.data_fetcher.fetch_data_sync(symbol, start_date, end_date, source='yfinance')

            # Load strategy
            strategy = self.strategy_loader.load_strategy(strategy_name, params)

            self.logger.info(f"Running backtest for {strategy_name}")
            results = self.backtester.run(strategy, data)

            self.logger.info(f"Backtest completed for {strategy_name}")
            return results
        except ConnectionError as ce:
            error_msg = f"Network error: {str(ce)}"
            self.logger.error(error_msg)
            return {"error": error_msg}
        except ValueError as ve:
            error_msg = f"Data error: {str(ve)}"
            self.logger.error(error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error in run_backtest: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    def get_available_strategies(self) -> list:
        return self.strategy_loader.list_available_strategies()

def create_backtesting_app():
    return BacktestingApp()

if __name__ == "__main__":
    app = create_backtesting_app()

    # Example usage
    strategy_name = "MA_CROSSOVER"
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    params = {
        "fast_period": 10,
        "slow_period": 30,
        "initial_capital": 10000,
        "risk_per_trade": 0.02
    }

    try:
        results = app.run_backtest(strategy_name, symbol, start_date, end_date, params)
        if "error" in results:
            print(f"Error running backtest: {results['error']}")
        else:
            print("Backtest Results:")
            print(f"Total Return: {results.get('total_return', 'N/A'):.2f}%")
            print(f"Sharpe Ratio: {results.get('sharpe_ratio', 'N/A'):.2f}")
            print(f"Max Drawdown: {results.get('max_drawdown', 'N/A'):.2f}%")
            print(f"Win Rate: {results.get('win_rate', 'N/A'):.2f}%")
    except Exception as e:
        print(f"Error running backtest: {str(e)}")