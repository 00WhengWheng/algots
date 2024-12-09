import unittest
from unittest.mock import patch, AsyncMock
import pandas as pd
from data.data_fetcher import DataFetcher

class TestDataFetcher(unittest.TestCase):

    @patch('data.data_fetcher.AlphaVantageAPI')
    @patch('data.data_fetcher.QuandlAPI')
    @patch('data.data_fetcher.YFinanceAPI')
    @patch('data.data_fetcher.CCXTProvider')
    def setUp(self, MockCCXTProvider, MockYFinanceAPI, MockQuandlAPI, MockAlphaVantageAPI):
        # Mock the API providers
        self.mock_alpha_vantage = MockAlphaVantageAPI.return_value
        self.mock_quandl = MockQuandlAPI.return_value
        self.mock_yfinance = MockYFinanceAPI.return_value
        self.mock_ccxt = MockCCXTProvider.return_value

        # Create an instance of DataFetcher
        self.fetcher = DataFetcher()

    @patch('data.data_fetcher.DataFetcher.save_data', return_value='mocked_file_path.csv')
    async def test_update_dataset_alpha_vantage(self, mock_save_data):
        # Mock the data returned by AlphaVantageAPI
        self.mock_alpha_vantage.get_daily_data = AsyncMock(return_value=pd.DataFrame({'price': [100, 101, 102]}))

        # Test the update_dataset method
        result = await self.fetcher.update_dataset('AAPL', source='alpha_vantage', interval='1d')
        self.assertEqual(result, 'mocked_file_path.csv')
        self.mock_alpha_vantage.get_daily_data.assert_awaited_once_with('AAPL')
        mock_save_data.assert_called_once()

    @patch('data.data_fetcher.DataFetcher.save_data', return_value='mocked_file_path.csv')
    async def test_update_dataset_quandl(self, mock_save_data):
        # Mock the data returned by QuandlAPI
        self.mock_quandl.get_stock_data = AsyncMock(return_value=pd.DataFrame({'price': [200, 201, 202]}))

        # Test the update_dataset method
        result = await self.fetcher.update_dataset('AAPL', source='quandl')
        self.assertEqual(result, 'mocked_file_path.csv')
        self.mock_quandl.get_stock_data.assert_awaited_once_with('AAPL')
        mock_save_data.assert_called_once()

    # Additional tests for yfinance and ccxt can be added similarly

if __name__ == '__main__':
    unittest.main()