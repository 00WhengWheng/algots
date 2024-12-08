def average_true_range(high, low, close, period=14):
    """
    Calculate the Average True Range (ATR).

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        period (int): Lookback period for ATR.
    
    Returns:
        numpy array: ATR values.
    """
    true_range = pd.concat([
        high - low,
        abs(high - close.shift(1)),
        abs(low - close.shift(1))
    ], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr
