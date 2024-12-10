import os
from dotenv import load_dotenv
import pandas as pd
import aiohttp
from typing import Optional
from datetime import datetime, timedelta

load_dotenv()

class AlphaVantageAPI:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"

    def _is_crypto(self, symbol: str) -> bool:
        """Check if the symbol is a cryptocurrency"""
        return '/' in symbol

    def _format_symbol(self, symbol: str) -> str:
        """Format symbol for Alpha Vantage API"""
        return symbol.replace('/', '') if self._is_crypto(symbol) else symbol

    async def fetch_data(self, symbol: str, start_date: str, end_date: str, interval: str = '1d') -> Optional[pd.DataFrame]:
        """Asynchronously fetch historical data from Alpha Vantage"""
        try:
            formatted_symbol = self._format_symbol(symbol)
            is_crypto = self._is_crypto(symbol)

            params = {
                "apikey": self.api_key,
                "symbol": formatted_symbol,
                "outputsize": "full",
            }

            if is_crypto:
                if interval == '1d':
                    params["function"] = "DIGITAL_CURRENCY_DAILY"
                    params["market"] = "USD"
                else:
                    raise ValueError("Intraday data for cryptocurrencies is not supported by Alpha Vantage")
            else:
                if interval == '1d':
                    params["function"] = "TIME_SERIES_DAILY"
                else:
                    params["function"] = "TIME_SERIES_INTRADAY"
                    params["interval"] = interval

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        raise ValueError(f"HTTP error {response.status}: {await response.text()}")
                    
                    data = await response.json()

                    if "Error Message" in data:
                        raise ValueError(data["Error Message"])

                    if "Note" in data:
                        raise ValueError(f"API limit reached: {data['Note']}")

                    time_series_key = next((key for key in data.keys() if key.startswith("Time Series")), None)
                    if not time_series_key:
                        raise ValueError(f"Unexpected API response format: {data.keys()}")
                    
                    df = pd.DataFrame(data[time_series_key]).T
                    df.index = pd.to_datetime(df.index)

                    if is_crypto:
                        df = df[['1a. open (USD)', '2a. high (USD)', '3a. low (USD)', '4a. close (USD)', '5. volume']]
                    else:
                        df = df[['1. open', '2. high', '3. low', '4. close', '5. volume']]

                    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    df = df.astype(float)

                    # Filter data based on start_date and end_date
                    start = pd.to_datetime(start_date)
                    end = pd.to_datetime(end_date)
                    df = df[(df.index >= start) & (df.index <= end)]

                    if df.empty:
                        raise ValueError(f"No data available for the specified date range: {start_date} to {end_date}")

                    return df

        except Exception as e:
            print(f"Error fetching data from Alpha Vantage: {e}")
            return None

    async def get_daily_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Fetch daily data for a given symbol"""
        return await self.fetch_data(symbol, start_date, end_date, interval='1d')

    async def get_intraday_data(self, symbol: str, start_date: str, end_date: str, interval: str = '1h') -> Optional[pd.DataFrame]:
        """Fetch intraday data for a given symbol and interval"""
        if self._is_crypto(symbol):
            raise ValueError("Intraday data for cryptocurrencies is not supported by Alpha Vantage")
        return await self.fetch_data(symbol, start_date, end_date, interval=interval)