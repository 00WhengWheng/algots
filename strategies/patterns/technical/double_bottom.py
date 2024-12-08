def double_bottom(low_prices, threshold=0.02):
    """
    Identify Double Bottom patterns (Reversal).

    Args:
        low_prices (list or numpy array): Low prices of the asset.
        threshold (float): Threshold for pattern similarity.
    
    Returns:
        list: Indices where Double Bottom patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(low_prices) - 1):
        if abs(low_prices[i - 1] - low_prices[i]) / low_prices[i - 1] < threshold:
            if low_prices[i - 2] < low_prices[i - 1] and low_prices[i] < low_prices[i + 1]:
                pattern_indices.append(i)
    return pattern_indices
