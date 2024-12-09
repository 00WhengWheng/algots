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

    async def fetch_data(self, dataset_code: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """Asynchronously fetch historical data from Quandl"""
        try:
            data = quandl.get(dataset_code, start_date=start_date, end_date=end_date)
            return data
        except Exception as e:
            print(f"Error fetching data from Quandl: {e}")
            return None

    async def get_stock_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """Fetch stock data for a given symbol"""
        dataset_code = f"WIKI/{symbol}"
        return await self.fetch_data(dataset_code, start_date, end_date)

    async def get_economic_data(self, indicator: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """Fetch economic data for a given indicator"""
        dataset_code = f"FRED/{indicator}"
        return await self.fetch_data(dataset_code, start_date, end_date)