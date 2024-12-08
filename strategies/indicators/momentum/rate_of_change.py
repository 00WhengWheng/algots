def rate_of_change(prices, period=14):
    """
    Calculate the Rate of Change (ROC).

    Args:
        prices (list or numpy array): Closing prices.
        period (int): Lookback period.
    
    Returns:
        numpy array: ROC values.
    """
    roc = (prices - prices.shift(period)) / prices.shift(period) * 100
    return roc
