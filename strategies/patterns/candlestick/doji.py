def doji(open_prices, close_prices, highs, lows, threshold=0.1):
    """
    Detect Doji candlestick pattern.

    Args:
        open_prices, close_prices, highs, lows (list): Sequences of OHLC values.
        threshold (float): Percentage range to consider a Doji.

    Returns:
        list: Indices of Doji candlestick patterns.
    """
    pattern_indices = []

    for i in range(len(open_prices)):
        body_size = abs(close_prices[i] - open_prices[i])
        candle_range = highs[i] - lows[i]
        if body_size <= candle_range * threshold:
            pattern_indices.append(i)

    return pattern_indices