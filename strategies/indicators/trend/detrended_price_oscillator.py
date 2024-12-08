def detrended_price_oscillator(prices, period=20):
    """
    Calculate Detrended Price Oscillator (DPO).

    Args:
        prices (list or numpy array): Closing prices.
        period (int): Lookback period.
    
    Returns:
        numpy array: DPO values.
    """
    ma = prices.rolling(window=period).mean()
    dpo = prices.shift(-period // 2 + 1) - ma
    return dpo
