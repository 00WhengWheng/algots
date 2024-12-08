def accumulation_distribution_line(high, low, close, volume):
    """
    Calculate the Accumulation/Distribution Line (A/D Line).

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        volume (list or numpy array): Volume data.
    
    Returns:
        numpy array: A/D Line values.
    """
    money_flow_multiplier = ((close - low) - (high - close)) / (high - low)
    money_flow_volume = money_flow_multiplier * volume
    adl = money_flow_volume.cumsum()
    return adl
