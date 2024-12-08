def money_flow_index(high_prices, low_prices, close_prices, volumes, period=14):
    """
    Calculate the Money Flow Index (MFI) indicator.

    Args:
        high_prices, low_prices, close_prices (list or numpy array): OHLC data.
        volumes (list or numpy array): Volume traded.
        period (int): Period for the MFI calculation.
    
    Returns:
        list: Money Flow Index values.
    """
    mfi = []
    for i in range(period, len(high_prices)):
        typical_price = (high_prices[i] + low_prices[i] + close_prices[i]) / 3
        money_flow = typical_price * volumes[i]
        mfi.append(sum(money_flow) / sum(volumes[i - period:i]))
    return mfi
