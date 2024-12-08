def double_top(high_prices, threshold=0.02):
    """
    Identify Double Top patterns (Reversal).

    Args:
        high_prices (list or numpy array): High prices of the asset.
        threshold (float): Threshold for pattern similarity.
    
    Returns:
        list: Indices where Double Top patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(high_prices) - 1):
        if abs(high_prices[i - 1] - high_prices[i]) / high_prices[i - 1] < threshold:
            if high_prices[i - 2] > high_prices[i - 1] and high_prices[i] > high_prices[i + 1]:
                pattern_indices.append(i)
    return pattern_indices
