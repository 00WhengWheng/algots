def detect_hammer(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Hammer candlestick patterns.

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Hammer patterns are detected.
    """
    hammer = []
    for i in range(len(open_prices)):
        body = abs(close_prices[i] - open_prices[i])
        lower_shadow = open_prices[i] - low_prices[i] if close_prices[i] > open_prices[i] else close_prices[i] - low_prices[i]
        upper_shadow = high_prices[i] - max(open_prices[i], close_prices[i])
        
        if lower_shadow > 2 * body and upper_shadow < 0.5 * body:
            hammer.append(i)
    return hammer
