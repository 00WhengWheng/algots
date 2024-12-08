def rounding_bottom(low_prices):
    """
    Identify Rounding Bottom patterns (Reversal).

    Args:
        low_prices (list or numpy array): Low prices of the asset.
    
    Returns:
        list: Indices where Rounding Bottom patterns are detected.
    """
    pattern_indices = []
    for i in range(3, len(low_prices) - 1):
        if low_prices[i - 2] > low_prices[i - 1] and low_prices[i - 1] < low_prices[i] and low_prices[i] < low_prices[i + 1]:
            pattern_indices.append(i)
    return pattern_indices
