import numpy as np

def historical_volatility(close_prices, period=14):
    """
    Calculate the Historical Volatility indicator.

    Args:
        close_prices (list or numpy array): Close prices of the asset.
        period (int): Period for the volatility calculation.
    
    Returns:
        list: Historical Volatility values.
    """
    returns = np.diff(np.log(close_prices))
    hvol = [np.std(returns[i - period:i]) * np.sqrt(period) for i in range(period, len(close_prices))]
    return hvol
