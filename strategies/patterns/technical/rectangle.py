def rectangle(high_prices, low_prices, threshold=0.02):
    """
    Identify Rectangle patterns (Continuation).

    Args:
        high_prices, low_prices (list or numpy array): High and Low prices of the asset.
        threshold (float): Threshold for pattern recognition.
    
    Returns:
        list: Indices where Rectangle patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(high_prices) - 1):
        if abs(high_prices[i] - high_prices[i - 1]) / high_prices[i - 1] < threshold and \
           abs(low_prices[i] - low_prices[i - 1]) / low_prices[i - 1] < threshold:
            pattern_indices.append(i)
    return pattern_indices
