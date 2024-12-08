def donchian_channels(high, low, period=20):
    """
    Calculate Donchian Channels.

    Args:
        high, low (list or numpy array): High and Low prices.
        period (int): Lookback period.
    
    Returns:
        tuple: (Upper Channel, Lower Channel).
    """
    upper_channel = high.rolling(window=period).max()
    lower_channel = low.rolling(window=period).min()
    return upper_channel, lower_channel
