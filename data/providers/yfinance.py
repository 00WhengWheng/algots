import yfinance as yf
import pandas as pd
from typing import Optional

class YFinanceAPI:
    async def fetch_data(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> Optional[pd.DataFrame]:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date, interval=interval)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            return df
        except Exception as e:
            print(f"Error fetching data from YFinance: {e}")
            return None

    async def get_data(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> Optional[pd.DataFrame]:
        return await self.fetch_data(symbol, start_date, end_date, interval)