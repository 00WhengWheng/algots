import numpy as np

def relative_strength_index(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI).

    Args:
        prices (pandas.Series): Closing prices.
        period (int): Lookback period for RSI calculation.

    Returns:
        pandas.Series: RSI values.
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    
    # Avoid division by zero
    rs = np.where(loss != 0, gain / loss, 100)
    
    rsi = 100 - (100 / (1 + rs))
    return rsi