def inverted_hammer(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Inverted Hammer candlestick patterns.

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Inverted Hammer patterns are detected.
    """
    pattern_indices = []
    for i in range(len(open_prices)):
        body = abs(close_prices[i] - open_prices[i])
        upper_shadow = high_prices[i] - max(open_prices[i], close_prices[i])
        lower_shadow = min(open_prices[i], close_prices[i]) - low_prices[i]
        
        if upper_shadow > 2 * body and lower_shadow < 0.5 * body:
            pattern_indices.append(i)
    return pattern_indices
