def bollinger_bands(prices, period=20, std_dev=2):
    """
    Calculate Bollinger Bands.

    Args:
        prices (list or numpy array): Closing prices.
        period (int): Lookback period for the moving average.
        std_dev (float): Number of standard deviations for the bands.
    
    Returns:
        tuple: (Middle Band, Upper Band, Lower Band).
    """
    middle_band = prices.rolling(window=period).mean()
    band_std = prices.rolling(window=period).std()
    upper_band = middle_band + (std_dev * band_std)
    lower_band = middle_band - (std_dev * band_std)
    return middle_band, upper_band, lower_band
