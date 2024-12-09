def calculate_vwap(high, low, close, volume):
    """
    Calculate Volume Weighted Average Price (VWAP).
    
    Args:
        high (pd.Series): High prices.
        low (pd.Series): Low prices.
        close (pd.Series): Close prices.
        volume (pd.Series): Volume data.

    Returns:
        pd.Series: VWAP values.
    """
    # Typical Price
    typical_price = (high + low + close) / 3

    # Cumulative Volume Weighted Typical Price
    vwap = (typical_price * volume).cumsum() / volume.cumsum()

    return vwap