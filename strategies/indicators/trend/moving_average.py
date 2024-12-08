import numpy as np

def moving_average(prices, window=20):
    """
    Calculate the Simple Moving Average (SMA).
    
    Args:
        prices (list or numpy array): Closing prices.
        window (int): Lookback period for the moving average.
    
    Returns:
        list: Moving average values.
    """
    return np.convolve(prices, np.ones(window)/window, mode='valid')
