def sideways_trend(close_prices, threshold=0.02):
    """
    Identify Sideways Trend patterns (Neutral).

    Args:
        close_prices (list or numpy array): Close prices of the asset.
        threshold (float): Threshold for pattern recognition.
    
    Returns:
        list: Indices where Sideways Trend patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(close_prices) - 1):
        if abs(close_prices[i] - close_prices[i - 1]) / close_prices[i - 1] < threshold:
            pattern_indices.append(i)
    return pattern_indices
