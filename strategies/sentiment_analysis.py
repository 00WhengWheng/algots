import pandas as pd
from ..utils.base_strategy import BaseStrategy

class SentimentAnalysis(BaseStrategy):
    def __init__(self, sentiment_column: str = 'Sentiment', threshold: float = 0.1):
        self.sentiment_column = sentiment_column
        self.threshold = threshold

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on sentiment analysis.

        :param data: Pandas DataFrame with price and sentiment data.
        :return: DataFrame with buy/sell signals.
        """
        if self.sentiment_column not in data.columns:
            raise ValueError(f"Missing required sentiment column: {self.sentiment_column}")

        data['Signal'] = 0
        data.loc[data[self.sentiment_column] > self.threshold, 'Signal'] = 1  # Buy for positive sentiment
        data.loc[data[self.sentiment_column] < -self.threshold, 'Signal'] = -1  # Sell for negative sentiment
        return data