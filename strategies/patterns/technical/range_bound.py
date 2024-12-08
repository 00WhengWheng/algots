def range_bound(high_prices, low_prices, threshold=0.02):
    """
    Identify Range-bound patterns (Neutral).

    Args:
        high_prices, low_prices (list or numpy array): High and Low prices of the asset.
        threshold (float): Threshold for pattern recognition.
    
    Returns:
        list: Indices where Range-bound patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(high_prices) - 1):
        if abs(high_prices[i] - low_prices[i]) / low_prices[i] < threshold:
            pattern_indices.append(i)
    return pattern_indices
