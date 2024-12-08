def stochastic_oscillator(high, low, close, period=14):
    """
    Calculate Stochastic Oscillator (%K).

    Args:
        high, low, close (list or numpy array): High, Low, and Close prices.
        period (int): Lookback period.
    
    Returns:
        tuple: %K (Stochastic Oscillator) and %D (Signal Line).
    """
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    percent_k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    percent_d = percent_k.rolling(window=3).mean()  # Signal line (3-period SMA of %K)
    return percent_k, percent_d
