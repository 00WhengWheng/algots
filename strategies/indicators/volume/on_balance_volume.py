def on_balance_volume(close, volume):
    """
    Calculate On-Balance Volume (OBV).

    Args:
        close (list or numpy array): Closing prices.
        volume (list or numpy array): Volume data.
    
    Returns:
        numpy array: OBV values.
    """
    obv = [0]
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            obv.append(obv[-1] + volume[i])
        elif close[i] < close[i - 1]:
            obv.append(obv[-1] - volume[i])
        else:
            obv.append(obv[-1])
    return obv
