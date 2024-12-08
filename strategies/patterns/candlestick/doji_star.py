def doji_star(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Doji Star candlestick patterns (Continuation).

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Doji Star patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(open_prices)):
        body = abs(close_prices[i] - open_prices[i])
        upper_shadow = high_prices[i] - max(open_prices[i], close_prices[i])
        lower_shadow = min(open_prices[i], close_prices[i]) - low_prices[i]

        if body < 0.1 * (high_prices[i] - low_prices[i]) and upper_shadow > 2 * body and lower_shadow > 2 * body:
            pattern_indices.append(i)
    return pattern_indices
