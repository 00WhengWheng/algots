import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def detect_triangle_pattern(data, lookback=20, tolerance=0.01):
    """
    Detect triangle patterns in a given price data.

    Args:
        data (pd.DataFrame): DataFrame containing 'High' and 'Low' prices.
        lookback (int): Number of periods to consider for the triangle pattern.
        tolerance (float): Tolerance level for deviations from the trendlines.

    Returns:
        pd.Series: Boolean Series indicating where triangle patterns occur.
    """
    highs = data['High']
    lows = data['Low']
    triangle_pattern = pd.Series(False, index=data.index)

    for i in range(lookback, len(data)):
        # Extract highs and lows for the lookback period
        recent_highs = highs[i-lookback:i].values
        recent_lows = lows[i-lookback:i].values
        time_index = np.arange(lookback)

        # Linear regression for highs and lows
        high_slope, high_intercept, _, _, _ = linregress(time_index, recent_highs)
        low_slope, low_intercept, _, _, _ = linregress(time_index, recent_lows)

        # Calculate trendlines
        trendline_highs = high_slope * time_index + high_intercept
        trendline_lows = low_slope * time_index + low_intercept

        # Check if highs and lows are within tolerance of their trendlines
        within_high_tolerance = np.all(np.abs(recent_highs - trendline_highs) < tolerance)
        within_low_tolerance = np.all(np.abs(recent_lows - trendline_lows) < tolerance)

        # Check for converging trendlines (triangle pattern)
        if within_high_tolerance and within_low_tolerance and high_slope < 0 and low_slope > 0:
            triangle_pattern.iloc[i] = True

    return triangle_pattern
