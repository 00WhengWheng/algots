def detect_trend_continuation(ama, price):
    """
    Detect trend continuation based on AMA slope and price relationship.
    Adaptive Moving Average Strategy:
    """
    ama_slope = ama.diff()
    continuation = (ama_slope > 0) & (price > ama)  # Bullish trend
    continuation |= (ama_slope < 0) & (price < ama)  # Bearish trend
    return continuation
