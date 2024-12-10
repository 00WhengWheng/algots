import os
from dotenv import load_dotenv
import pandas as pd
import quandl
from typing import Optional

load_dotenv()

class QuandlAPI:
    def __init__(self):
        self.api_key = os.getenv('QUANDL_API_KEY')
        quandl.ApiConfig.api_key = self.api_key

    async def fetch_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        try:
            df = quandl.get(f"WIKI/{symbol}", start_date=start_date, end_date=end_date)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            return df
        except Exception as e:
            print(f"Error fetching data from Quandl: {e}")
            return None

    async def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        return await self.fetch_data(symbol, start_date, end_date)