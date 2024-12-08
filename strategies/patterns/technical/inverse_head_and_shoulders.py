def inverse_head_and_shoulders(low_prices):
    """
    Identify Inverse Head and Shoulders patterns (Reversal).

    Args:
        low_prices (list or numpy array): Low prices of the asset.
    
    Returns:
        list: Indices where Inverse Head and Shoulders patterns are detected.
    """
    pattern_indices = []
    for i in range(2, len(low_prices) - 1):
        left_shoulder = low_prices[i - 2] > low_prices[i - 1]
        head = low_prices[i - 1] < low_prices[i] and low_prices[i - 1] < low_prices[i + 1]
        right_shoulder = low_prices[i + 1] > low_prices[i]
        
        if left_shoulder and head and right_shoulder:
            pattern_indices.append(i)
    return pattern_indices
