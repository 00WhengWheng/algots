def volume_price_trend(close_prices, volumes):
    """
    Calculate the Volume Price Trend (VPT) indicator.

    Args:
        close_prices (list or numpy array): Close prices of the asset.
        volumes (list or numpy array): Volume traded.
    
    Returns:
        list: Volume Price Trend values.
    """
    vpt = [0]
    for i in range(1, len(close_prices)):
        change_percent = (close_prices[i] - close_prices[i - 1]) / close_prices[i - 1]
        vpt.append(vpt[-1] + change_percent * volumes[i])
    return vpt
