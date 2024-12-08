def chaikin_money_flow(high, low, close, volume, period=20):
    """
    Calculate Chaikin Money Flow (CMF).

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        volume (list or numpy array): Volume data.
        period (int): Lookback period for CMF.
    
    Returns:
        numpy array: CMF values.
    """
    money_flow_multiplier = ((close - low) - (high - close)) / (high - low)
    money_flow_volume = money_flow_multiplier * volume
    cmf = money_flow_volume.rolling(window=period).sum() / volume.rolling(window=period).sum()
    return cmf
