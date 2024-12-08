def broadening_formation(high_prices, low_prices, threshold=0.02):
    """
    Identify Broadening Formation patterns (Reversal).

    Args:
        high_prices, low_prices (list or numpy array): High and Low prices of the asset.
        threshold (float): Threshold for pattern recognition.
    
    Returns:
        list: Indices where Broadening Formation patterns are detected.
    """
    pattern_indices = []
    for i in range(3, len(high_prices) - 1):
        if high_prices[i - 2] < high_prices[i - 1] and high_prices[i] > high_prices[i + 1] and \
           low_prices[i - 2] > low_prices[i - 1] and low_prices[i] < low_prices[i + 1]:
            pattern_indices.append(i)
    return pattern_indices
