def morning_star(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Morning Star candlestick patterns.

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Morning Star patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(open_prices)):
        first_candle = close_prices[i - 2] < open_prices[i - 2]
        second_candle = close_prices[i - 1] < open_prices[i - 1] and abs(close_prices[i - 1] - open_prices[i - 1]) < abs(close_prices[i - 2] - open_prices[i - 2])
        third_candle = close_prices[i] > open_prices[i] and close_prices[i] > close_prices[i - 2]

        if first_candle and second_candle and third_candle:
            pattern_indices.append(i)
    return pattern_indices
