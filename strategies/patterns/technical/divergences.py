def detect_divergences(price, ama):
    """
    Detect divergences between AMA and price trend.
    """
    price_slope = price.diff()
    ama_slope = ama.diff()
    divergences = (price_slope * ama_slope < 0)  # Opposite directions
    return divergences
