import yfinance as yf
import pandas as pd
from typing import Optional

class YFinanceAPI:
    async def get_data(self, symbol: str, interval: str = '1d') -> Optional[pd.DataFrame]:
        """Fetch data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="max", interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching data from Yahoo Finance: {e}")
            return None