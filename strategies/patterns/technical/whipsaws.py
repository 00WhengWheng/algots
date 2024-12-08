def detect_whipsaws(ama, price, threshold=0.02):
    """
    Detect whipsaws when price repeatedly crosses AMA in a short period.
    """
    crossovers = (price.shift(1) < ama.shift(1)) & (price > ama) | \
                 (price.shift(1) > ama.shift(1)) & (price < ama)
    whipsaws = crossovers.rolling(window=5).sum() > 3  # Customize window
    return whipsaws
