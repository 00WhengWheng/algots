from data.data_fetcher import DataFetcher

def test_data_collection():
    # Initialize DataFetcher
    fetcher = DataFetcher()
    
    # Test different data sources and timeframes
    test_cases = [
        ('BTC/USD', 'exchange', '1h'),
        ('AAPL', 'alpha_vantage', '1d'),
        ('WIKI/AAPL', 'quandl', None)
    ]
    
    for symbol, source, timeframe in test_cases:
        print(f"\nTesting {source} for {symbol} @ {timeframe}")
        
        # Fetch data
        data = None
        if source == 'exchange':
            data = fetcher.fetch_ohlcv(symbol, timeframe)
        elif source == 'alpha_vantage':
            data = fetcher.fetch_alpha_vantage(symbol, timeframe)
        elif source == 'quandl':
            data = fetcher.fetch_quandl(symbol)
            
        if data is not None:
            print(f"Successfully fetched {len(data)} rows")
            print("Data preview:")
            print(data.head())
            
            # Save data
            filename = fetcher.save_data(data, symbol, source)
            print(f"Data saved to: {filename}")
        else:
            print("Failed to fetch data")

if __name__ == "__main__":
    test_data_collection()
    