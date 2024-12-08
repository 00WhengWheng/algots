def keltner_channels(high, low, close, period=20, multiplier=2):
    """
    Calculate Keltner Channels.

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        period (int): Lookback period for the moving average.
        multiplier (float): Multiplier for the ATR.
    
    Returns:
        tuple: (Middle Band, Upper Band, Lower Band).
    """
    typical_price = (high + low + close) / 3
    middle_band = typical_price.rolling(window=period).mean()
    true_range = pd.concat([
        high - low,
        abs(high - close.shift(1)),
        abs(low - close.shift(1))
    ], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    upper_band = middle_band + (multiplier * atr)
    lower_band = middle_band - (multiplier * atr)
    return middle_band, upper_band, lower_band
