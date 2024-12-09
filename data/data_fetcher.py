import os
from dotenv import load_dotenv
import pandas as pd
import ccxt
import asyncio
from datetime import datetime
from .providers.alpha_vantage import AlphaVantageAPI
from .providers.quandl import QuandlAPI
from .providers.yfinance import YFinanceAPI
from .providers.ccxt_provider import CCXTProvider

load_dotenv()

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

    async def fetch_data(self, symbol: str, source: str, interval: str) -> pd.DataFrame:
        try:
            if source == 'alpha_vantage':
                return await self.fetch_alpha_vantage_data(symbol, interval)
            elif source == 'quandl':
                return await self.quandl.get_stock_data(symbol)
            elif source == 'yfinance':
                return await self.yfinance.get_data(symbol, interval)
            elif source == 'ccxt':
                return await self.ccxt.fetch_ohlcv(symbol, interval)
            else:
                raise ValueError(f"Unsupported data source: {source}")
        except Exception as e:
            print(f"Error fetching data for {symbol} from {source}: {e}")
            return None

    async def fetch_alpha_vantage_data(self, symbol: str, interval: str) -> pd.DataFrame:
        try:
            if interval == '1d':
                return await self.alpha_vantage.get_daily_data(symbol)
            else:
                return await self.alpha_vantage.get_intraday_data(symbol, interval)
        except Exception as e:
            print(f"Error fetching Alpha Vantage data for {symbol} with interval {interval}: {e}")
            return None

    async def update_dataset(self, symbol: str, source: str = 'alpha_vantage', interval: str = '1d') -> str:
        data = await self.fetch_data(symbol, source, interval)
        if data is not None:
            return self.save_data(data, symbol, source)
        else:
            print(f"No data retrieved for {symbol} from {source}")
            return None

    async def bulk_update(self, symbols, source='alpha_vantage', interval='1d'):
        tasks = [self.update_dataset(symbol, source, interval) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error updating dataset for {symbols[i]}: {result}")
        return results

async def main():
    fetcher = DataFetcher()

    sources = {
        'alpha_vantage': ['AAPL', 'GOOGL', 'MSFT'],
        'quandl': ['AAPL', 'GOOGL', 'MSFT'],
        'yfinance': ['AAPL', 'GOOGL', 'MSFT'],
        'ccxt': ['BTC/USDT', 'ETH/USDT']
    }
    intervals = {
        'alpha_vantage': '1d',
        'quandl': '1d',
        'yfinance': '1d',
        'ccxt': '1h'
    }

    for source, symbols in sources.items():
        results = await fetcher.bulk_update(symbols, source=source, interval=intervals[source])
        print(f"Updated {len(results)} datasets from {source.capitalize()}")

if __name__ == "__main__":
    asyncio.run(main())
