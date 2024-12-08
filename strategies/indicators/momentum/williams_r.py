def williams_r(high, low, close, period=14):
    """
    Calculate Williams %R.

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        period (int): Lookback period.
    
    Returns:
        numpy array: Williams %R values.
    """
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    percent_r = (highest_high - close) / (highest_high - lowest_low) * -100
    return percent_r
