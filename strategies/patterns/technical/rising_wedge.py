def rising_wedge(high_prices, low_prices, threshold=0.05):
    """
    Identify Rising Wedge patterns (Continuation).

    Args:
        high_prices, low_prices (list or numpy array): High and Low prices of the asset.
        threshold (float): Threshold for pattern recognition.
    
    Returns:
        list: Indices where Rising Wedge patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(high_prices) - 1):
        upper_trend = high_prices[i - 2] < high_prices[i - 1] and high_prices[i] < high_prices[i + 1]
        lower_trend = low_prices[i - 2] > low_prices[i - 1] and low_prices[i] > low_prices[i + 1]
        
        if upper_trend and lower_trend:
            pattern_indices.append(i)
    return pattern_indices
