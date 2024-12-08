def macd_signal_line(prices, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate MACD and Signal Line.
    
    Args:
        prices (list or numpy array): Closing prices.
        fast_period (int): Fast EMA period.
        slow_period (int): Slow EMA period.
        signal_period (int): Signal line EMA period.
    
    Returns:
        tuple: MACD line, Signal line.
    """
    ema_fast = prices.ewm(span=fast_period).mean()
    ema_slow = prices.ewm(span=slow_period).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal_period).mean()
    return macd, signal_line
