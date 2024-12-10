import os
import aiohttp
import pandas as pd
from typing import Optional

class AlphaVantageAPI:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is not set")
        self.base_url = "https://www.alphavantage.co/query"

    async def fetch_data(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> Optional[pd.DataFrame]:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "full"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()
                print(f"API Response: {data}")  # Debug print
                if "Error Message" in data:
                    raise ValueError(data["Error Message"])

                time_series = data.get("Time Series (Daily)")
                if not time_series:
                    raise ValueError(f"Unexpected API response format: {data.keys()}")

                df = pd.DataFrame(time_series).T
                df.index = pd.to_datetime(df.index)
                df = df[(df.index >= start_date) & (df.index <= end_date)]
                return df

    async def get_daily_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        return await self.fetch_data(symbol, start_date, end_date)