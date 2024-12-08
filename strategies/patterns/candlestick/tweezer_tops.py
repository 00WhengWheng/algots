def tweezer_tops(open_prices, close_prices, high_prices, low_prices):
    """
    Identify Tweezer Tops candlestick patterns (Reversal).

    Args:
        open_prices, close_prices, high_prices, low_prices (list or numpy array): OHLC data.
    
    Returns:
        list: Indices where Tweezer Tops patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(open_prices)):
        if high_prices[i] == high_prices[i - 1] and close_prices[i] < open_prices[i] and close_prices[i - 1] < open_prices[i - 1]:
            pattern_indices.append(i)
    return pattern_indices
