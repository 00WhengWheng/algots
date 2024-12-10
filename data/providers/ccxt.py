import ccxt
import pandas as pd
from typing import Optional
from datetime import datetime

class CCXTProvider:
    def __init__(self, exchange: str = 'binance'):
        self.exchange = getattr(ccxt, exchange)()

    async def fetch_ohlcv(self, symbol: str, timeframe: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        try:
            # Convert start_date and end_date to milliseconds timestamp
            start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
            end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, start_timestamp, None)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Filter data based on start_date and end_date
            df = df[(df.index >= start_date) & (df.index <= end_date)]
            
            return df
        except Exception as e:
            print(f"Error fetching OHLCV data for {symbol} with timeframe {timeframe}: {e}")
            return None