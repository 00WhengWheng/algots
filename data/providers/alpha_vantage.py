import os
from dotenv import load_dotenv
import pandas as pd
import aiohttp
from typing import Optional

load_dotenv()

class AlphaVantageAPI:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"

    async def fetch_data(self, symbol: str, interval: str = '1d', outputsize: str = 'full') -> Optional[pd.DataFrame]:
        """Asynchronously fetch historical data from Alpha Vantage"""
        try:
            params = {
                "apikey": self.api_key,
                "symbol": symbol,
                "outputsize": outputsize,
            }

            if interval == '1d':
                params["function"] = "TIME_SERIES_DAILY"
            else:
                params["function"] = "TIME_SERIES_INTRADAY"
                params["interval"] = interval

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    data = await response.json()

                    if "Error Message" in data:
                        raise ValueError(data["Error Message"])

                    time_series_key = list(data.keys())[1]
                    df = pd.DataFrame(data[time_series_key]).T
                    df.index = pd.to_datetime(df.index)
                    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    df = df.astype(float)
                    return df

        except Exception as e:
            print(f"Error fetching data from Alpha Vantage: {e}")
            return None

    async def get_daily_data(self, symbol: str, outputsize: str = 'full') -> Optional[pd.DataFrame]:
        """Fetch daily data for a given symbol"""
        return await self.fetch_data(symbol, interval='1d', outputsize=outputsize)

    async def get_intraday_data(self, symbol: str, interval: str = '1h', outputsize: str = 'full') -> Optional[pd.DataFrame]:
        """Fetch intraday data for a given symbol and interval"""
        return await self.fetch_data(symbol, interval=interval, outputsize=outputsize)