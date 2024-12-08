def head_and_shoulders(high_prices):
    """
    Identify Head and Shoulders patterns (Reversal).

    Args:
        high_prices (list or numpy array): High prices of the asset.
    
    Returns:
        list: Indices where Head and Shoulders patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(high_prices) - 1):
        left_shoulder = high_prices[i - 2] < high_prices[i - 1]
        head = high_prices[i - 1] > high_prices[i] and high_prices[i - 1] > high_prices[i + 1]
        right_shoulder = high_prices[i + 1] < high_prices[i]
        
        if left_shoulder and head and right_shoulder:
            pattern_indices.append(i)
    return pattern_indices
