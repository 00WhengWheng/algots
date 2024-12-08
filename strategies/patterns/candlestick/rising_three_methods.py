def rising_three_methods(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Rising Three Methods candlestick patterns (Continuation).

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Rising Three Methods patterns are detected.
    """
    pattern_indices = []
    for i in range(3, len(open_prices)):
        first_candle = close_prices[i - 3] > open_prices[i - 3]
        second_candle = close_prices[i - 2] < open_prices[i - 2]
        third_candle = close_prices[i - 1] < open_prices[i - 1]
        fourth_candle = close_prices[i] > open_prices[i]

        if first_candle and second_candle and third_candle and fourth_candle:
            pattern_indices.append(i)
    return pattern_indices
