import pandas as pd
import ccxt
from typing import Optional
from datetime import datetime

class CCXTProvider:
    def __init__(self, exchange: str = 'binance'):
        self.exchange = getattr(ccxt, exchange)()

    async def fetch_data(self, symbol: str, start_date: str, end_date: str, timeframe: str = '1d') -> Optional[pd.DataFrame]:
        try:
            since = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
            end = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)

            ohlcv = []
            while since < end:
                data = await self.exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
                ohlcv.extend(data)
                if len(data) == 0:
                    break
                since = data[-1][0] + 1

            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df = df[(df.index >= start_date) & (df.index <= end_date)]
            return df

        except Exception as e:
            print(f"Error fetching data from CCXT: {e}")
            return None