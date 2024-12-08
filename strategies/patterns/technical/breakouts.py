def detect_breakouts(price, ama):
    """
    Detect breakouts when the price deviates significantly from AMA.
    """
    breakout = abs(price - ama) > (price * 0.02)  # Customize 2% threshold
    return breakout
