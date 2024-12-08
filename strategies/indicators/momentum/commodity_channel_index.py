def commodity_channel_index(high, low, close, period=20):
    """
    Calculate the Commodity Channel Index (CCI).

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        period (int): Lookback period.
    
    Returns:
        numpy array: CCI values.
    """
    typical_price = (high + low + close) / 3
    moving_average = typical_price.rolling(window=period).mean()
    mean_deviation = typical_price.rolling(window=period).apply(lambda x: abs(x - x.mean()).mean(), raw=True)
    cci = (typical_price - moving_average) / (0.015 * mean_deviation)
    return cci
