def relative_strenght_index(prices, period=14):
    """
    Calculate the Relative Strength Index (RSI).

    Args:
        prices (list or numpy array): Closing prices.
        period (int): Lookback period for RSI calculation.

    Returns:
        numpy array: RSI values.
    """
    delta = prices.diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
