import pandas as pd
import numpy as np

def time_weighted_average_price(data, time_period):
    """
    Calculate Time Weighted Average Price (TWAP).

    Args:
        data (pd.DataFrame): DataFrame with 'Open', 'High', 'Low', 'Close' columns and a datetime index.
        time_period (int): Number of periods for TWAP calculation.

    Returns:
        pd.Series: TWAP values.
    """
    # Calculate typical price for each period
    typical_price = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4

    # Calculate cumulative sum of typical price
    cumulative_price = typical_price.cumsum()

    # Calculate TWAP
    twap = (cumulative_price - cumulative_price.shift(time_period)) / time_period

    return twap

def plot_twap(data, twap):
    """
    Plot the TWAP alongside the closing price.

    Args:
        data (pd.DataFrame): DataFrame with 'Close' column and a datetime index.
        twap (pd.Series): TWAP values.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.plot(twap.index, twap, label='TWAP')
    plt.title('Time Weighted Average Price (TWAP)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()