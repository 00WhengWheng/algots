from data_collector import DataCollector
from config.settings import TRADING_PAIRS

def main():
    collector = DataCollector()
    
    # Collect data for all trading pairs
    for pair in TRADING_PAIRS:
        print(f"Collecting data for {pair}")
        
        # Collect daily data
        daily_file = collector.update_dataset(pair, source='alpha_vantage', interval='1d')
        if daily_file:
            print(f"Daily data saved to {daily_file}")
            
        # Collect hourly data
        hourly_file = collector.update_dataset(pair, source='alpha_vantage', interval='1h')
        if hourly_file:
            print(f"Hourly data saved to {hourly_file}")

if __name__ == "__main__":
    main()
