import pandas as pd
import yfinance as yf
import asyncio
import logging
import requests
from requests.exceptions import RequestException

class DataFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self, symbol: str, start_date: str, end_date: str, source: str = 'yfinance', interval: str = '1d') -> pd.DataFrame:
        if source == 'yfinance':
            return self.fetch_data_yfinance(symbol, start_date, end_date, interval)
        else:
            raise ValueError(f"Unsupported data source: {source}")

    def fetch_data_sync(self, symbol: str, start_date: str, end_date: str, source: str = 'yfinance', interval: str = '1d') -> pd.DataFrame:
        return asyncio.run(self.fetch_data(symbol, start_date, end_date, source, interval))

    def fetch_data_yfinance(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> pd.DataFrame:
        try:
            self._check_internet_connection()
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            if data.empty:
                raise ValueError(f"No data available for {symbol} in the specified date range.")
            return data
        except RequestException as e:
            self.logger.error(f"Network error while fetching data for {symbol}: {str(e)}")
            raise ConnectionError(f"Network error: Unable to connect to Yahoo Finance. Please check your internet connection.")
        except ValueError as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error fetching data for {symbol}: {str(e)}")
            raise RuntimeError(f"An unexpected error occurred while fetching data for {symbol}: {str(e)}")

    def _check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=5)
        except RequestException:
            raise ConnectionError("No internet connection available.")