def marubozu(candle_bodies, threshold=0.05):
    """
    Identify Marubozu candlestick patterns.

    Args:
        candle_bodies (list): List of candle body lengths as the difference between open and close prices.
        threshold (float): Threshold to define a Marubozu candlestick.
    
    Returns:
        list: Indices where Marubozu patterns are detected.
    """
    pattern_indices = []
    for i in range(1, len(candle_bodies) - 1):
        if candle_bodies[i] / max(candle_bodies[i - 1], candle_bodies[i + 1]) > threshold:
            pattern_indices.append(i)
    return pattern_indices
