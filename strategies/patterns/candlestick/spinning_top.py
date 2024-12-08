def spinning_top(candle_bodies, threshold=0.03):
    """
    Identify Spinning Top candlestick patterns.

    Args:
        candle_bodies (list): List of candle body lengths as the difference between open and close prices.
        threshold (float): Threshold to define a Spinning Top candlestick.
    
    Returns:
        list: Indices where Spinning Top patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(candle_bodies) - 1):
        if candle_bodies[i] / (candle_bodies[i - 1] + candle_bodies[i + 1]) < threshold:
            pattern_indices.append(i)
    return pattern_indices
