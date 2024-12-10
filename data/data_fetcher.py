import pandas as pd
import os
from datetime import datetime
import asyncio
from .providers.alpha_vantage import AlphaVantageAPI
from .providers.quandl import QuandlAPI
from .providers.yfinance import YFinanceAPI
from .providers.ccxt import CCXTProvider

class DataFetcher:
    def __init__(self, exchange='binance'):
        self.alpha_vantage = AlphaVantageAPI()
        self.quandl = QuandlAPI()
        self.yfinance = YFinanceAPI()
        self.ccxt = CCXTProvider(exchange)
        os.makedirs('data/historical', exist_ok=True)

    def save_data(self, data: pd.DataFrame, symbol: str, source: str) -> str:
        filename = f"data/historical/{source}_{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
        data.to_csv(filename)
        return filename

    async def fetch_data(self, symbol: str, start_date: str, end_date: str, source: str, interval: str) -> pd.DataFrame:
        try:
            if source == 'alpha_vantage':
                return await self.fetch_alpha_vantage_data(symbol, interval, start_date, end_date)
            elif source == 'quandl':
                return await self.quandl.get_stock_data(symbol, start_date, end_date)
            elif source == 'yfinance':
                return await self.yfinance.get_data(symbol, interval, start_date, end_date)
            elif source == 'ccxt':
                return await self.ccxt.fetch_ohlcv(symbol, interval, start_date, end_date)
            else:
                raise ValueError(f"Unsupported data source: {source}")
        except Exception as e:
            print(f"Error fetching data for {symbol} from {source}: {e}")
            return None

    async def fetch_alpha_vantage_data(self, symbol: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            is_crypto = '/' in symbol  # Simple check to determine if it's a cryptocurrency
    
            if is_crypto:
                if interval != '1d':
                    raise ValueError("Intraday data for cryptocurrencies is not supported by Alpha Vantage")
                data = await self.alpha_vantage.get_daily_data(symbol, start_date, end_date)
            else:
                if interval == '1d':
                    data = await self.alpha_vantage.get_daily_data(symbol, start_date, end_date)
                else:
                    data = await self.alpha_vantage.get_intraday_data(symbol, start_date, end_date, interval)
            
            if data is not None:
                # Filter data based on start_date and end_date
                data = data[(data.index >= start_date) & (data.index <= end_date)]
            return data
        except ValueError as e:
            print(f"Error fetching Alpha Vantage data for {symbol} with interval {interval}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching Alpha Vantage data for {symbol} with interval {interval}: {e}")
            return None

    async def update_dataset(self, symbol: str, start_date: str, end_date: str, source: str = 'alpha_vantage', interval: str = '1d') -> str:
        data = await self.fetch_data(symbol, start_date, end_date, source, interval)
        if data is not None:
            return self.save_data(data, symbol, source)
        else:
            print(f"No data retrieved for {symbol} from {source}")
            return None

    async def bulk_update(self, symbols, start_date, end_date, source='alpha_vantage', interval='1d'):
        tasks = [self.update_dataset(symbol, start_date, end_date, source, interval) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error updating dataset for {symbols[i]}: {result}")
        return results

# The main function remains the same