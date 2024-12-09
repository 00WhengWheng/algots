import ccxt
import pandas as pd
from typing import Optional

class CCXTProvider:
    def __init__(self, exchange: str = 'binance'):
        self.exchange = getattr(ccxt, exchange)()

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1d', since: Optional[int] = None, limit: int = 1000) -> Optional[pd.DataFrame]:
        """Fetch OHLCV data from the exchange"""
        try:
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data from CCXT: {e}")
            return None