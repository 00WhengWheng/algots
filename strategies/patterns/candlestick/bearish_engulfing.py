def bearish_engulfing(open_prices, close_prices):
    """
    Identify Bearish Engulfing candlestick patterns.

    Args:
        open_prices, close_prices (list or numpy array): Open and Close prices.
    
    Returns:
        list: Indices where Bearish Engulfing patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(open_prices)):
        if close_prices[i - 1] > open_prices[i - 1] and close_prices[i] < open_prices[i] and \
           open_prices[i] > close_prices[i - 1] and close_prices[i] < open_prices[i - 1]:
            pattern_indices.append(i)
    return pattern_indices
