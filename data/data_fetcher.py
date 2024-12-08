import os
from dotenv import load_dotenv
import pandas as pd
import ccxt
import requests
from alpha_vantage.timeseries import TimeSeries
import quandl
from datetime import datetime, timedelta

load_dotenv()

class DataFetcher:
    def __init__(self, exchange='binance'):
        # Exchange API for real-time data
        self.exchange = getattr(ccxt, exchange)()
        
        # External data providers
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.quandl_key = os.getenv('QUANDL_API_KEY')
        self.ts = TimeSeries(key=self.alpha_vantage_key, output_format='pandas')
        quandl.ApiConfig.api_key = self.quandl_key
        
        # Create data directory if not exists
        os.makedirs('data/historical', exist_ok=True)

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=1000):
        """Fetch real-time OHLCV data from exchange"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching exchange data: {e}")
            return None

    def fetch_alpha_vantage(self, symbol: str, interval: str = '1h', outputsize: str = 'full'):
        """Fetch historical data from Alpha Vantage"""
        try:
            if interval == '1d':
                data, _ = self.ts.get_daily(symbol=symbol, outputsize=outputsize)
            else:
                data, _ = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
            
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            return data
        except Exception as e:
            print(f"Error fetching from Alpha Vantage: {e}")
            return None

    def fetch_quandl(self, dataset_code: str, start_date: str = None, end_date: str = None):
        """Fetch historical data from Quandl"""
        try:
            data = quandl.get(dataset_code, start_date=start_date, end_date=end_date)
            return data
        except Exception as e:
            print(f"Error fetching from Quandl: {e}")
            return None

    def save_data(self, data: pd.DataFrame, symbol: str, source: str):
        """Save data to CSV file"""
        filename = f"data/historical/{source}_{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
        data.to_csv(filename)
        return filename

    def load_historical(self, symbol: str, source: str, start_date: str = None, end_date: str = None):
        """Load historical data from saved files"""
        pattern = f"data/historical/{source}_{symbol}_*.csv"
        files = sorted(glob.glob(pattern))
        if not files:
            return None
        
        # Load most recent file
        data = pd.read_csv(files[-1], index_col=0, parse_dates=True)
        
        # Filter by date range if specified
        if start_date:
            data = data[data.index >= start_date]
        if end_date:
            data = data[data.index <= end_date]
            
        return data

    def update_dataset(self, symbol: str, source: str = 'alpha_vantage', interval: str = '1d'):
        """Update dataset for a given symbol"""
        if source == 'alpha_vantage':
            data = self.fetch_alpha_vantage(symbol, interval)
        elif source == 'quandl':
            data = self.fetch_quandl(symbol)
        elif source == 'exchange':
            data = self.fetch_ohlcv(symbol, interval)
        
        if data is not None:
            return self.save_data(data, symbol, source)
        return None