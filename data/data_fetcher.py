import ccxt
import pandas as pd
from datetime import datetime

class DataFetcher:
    def __init__(self, exchange='binance'):
        self.exchange = getattr(ccxt, exchange)()
        
    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=1000):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
