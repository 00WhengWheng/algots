import pandas as pd
import numpy as np

def detect_flag_pattern(data: pd.DataFrame, column: str = 'Close', window: int = 20, threshold: float = 0.03) -> pd.DataFrame:
    """
    Detects Flag patterns in price data.

    :param data: Pandas DataFrame with price data.
    :param column: Name of the column to analyze for patterns (default: 'Close').
    :param window: Number of periods to consider for flag pattern (default: 20).
    :param threshold: Threshold for price movement to be considered significant (default: 0.03).
    :return: DataFrame with a new column 'Flag_Pattern' indicating pattern presence.
    """
    data = data.copy()
    data['Flag_Pattern'] = False

    # Calculate price change
    data['Price_Change'] = data[column].pct_change()

    # Calculate trend
    data['Trend'] = np.where(data[column].diff() > 0, 1, -1)

    for i in range(window, len(data)):
        window_data = data.iloc[i-window:i]

        # Check for strong initial move
        initial_move = abs(window_data['Price_Change'].iloc[0]) > threshold

        # Check for consolidation (flag)
        consolidation = (window_data['Price_Change'].abs() < threshold).all()

        # Check for consistent trend before the flag
        consistent_trend = (window_data['Trend'].iloc[:-5] == window_data['Trend'].iloc[0]).all()

        # Check for narrowing price range
        high_prices = window_data[column].rolling(window=5).max()
        low_prices = window_data[column].rolling(window=5).min()
        narrowing_range = (high_prices.iloc[-1] - low_prices.iloc[-1]) < (high_prices.iloc[0] - low_prices.iloc[0])

        if initial_move and consolidation and consistent_trend and narrowing_range:
            data.loc[data.index[i], 'Flag_Pattern'] = True

    return data

def plot_flag_pattern(data: pd.DataFrame, column: str = 'Close'):
    """
    Plots the price data with flag patterns highlighted.

    :param data: Pandas DataFrame with price data and 'Flag_Pattern' column.
    :param column: Name of the column to plot (default: 'Close').
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data[column], label='Price')
    plt.scatter(data[data['Flag_Pattern']].index, data[data['Flag_Pattern']][column], 
                color='red', marker='^', s=100, label='Flag Pattern')
    plt.title('Flag Pattern Detection')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Example usage:
# data = pd.read_csv('your_price_data.csv', parse_dates=['Date'], index_col='Date')
# data_with_patterns = detect_flag_pattern(data)
# plot_flag_pattern(data_with_patterns)