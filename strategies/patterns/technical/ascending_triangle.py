def ascending_triangle(high_prices, low_prices, threshold=0.05):
    """
    Identify Ascending Triangle patterns (Continuation).

    Args:
        high_prices, low_prices (list or numpy array): High and Low prices of the asset.
        threshold (float): Threshold for pattern recognition.
    
    Returns:
        list: Indices where Ascending Triangle patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(high_prices) - 1):
        upper_trend = high_prices[i - 2] < high_prices[i - 1] and high_prices[i] < high_prices[i + 1]
        lower_support = low_prices[i - 2] <= low_prices[i - 1] and low_prices[i] <= low_prices[i + 1]
        
        if upper_trend and lower_support:
            pattern_indices.append(i)
    return pattern_indices
