def piercing_line(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Piercing Line candlestick patterns (Reversal).

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Piercing Line patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(open_prices)):
        first_candle = close_prices[i - 1] < open_prices[i - 1]
        second_candle = close_prices[i] > open_prices[i] and close_prices[i] > (open_prices[i - 1] + close_prices[i - 1]) / 2

        if first_candle and second_candle:
            pattern_indices.append(i)
    return pattern_indices
