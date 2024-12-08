import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from patterns.technical import head_and_shoulders
from indicators.trend import moving_average

# Adaptive Moving Average (AMA/KAMA) Calculation
def adaptive_moving_average(prices, period=10, fast_ema=2, slow_ema=30):
    """
    Calculates the Adaptive Moving Average (KAMA).

    Args:
        prices (pd.Series): Price series.
        period (int): Look-back period for efficiency ratio (ER).
        fast_ema (int): Fastest smoothing constant EMA period.
        slow_ema (int): Slowest smoothing constant EMA period.

    Returns:
        pd.Series: AMA values.
    """
    change = prices.diff(period).abs()
    volatility = prices.diff().abs().rolling(period).sum()

    # Efficiency Ratio (ER)
    er = change / volatility
    er = er.replace([np.inf, -np.inf], 0).fillna(0)

    # Smoothing constant (SC)
    fast_sc = 2 / (fast_ema + 1)
    slow_sc = 2 / (slow_ema + 1)
    sc = (er * (fast_sc - slow_sc) + slow_sc) ** 2

    # AMA Calculation
    ama = prices.copy()
    for i in range(1, len(prices)):
        ama.iloc[i] = ama.iloc[i - 1] + sc.iloc[i] * (prices.iloc[i] - ama.iloc[i - 1])

    return ama

# Example Usage
def main():
    # Generate synthetic data
    np.random.seed(42)
    data = pd.Series(100 + np.cumsum(np.random.normal(0, 1, 300)))  # Simulated price data

    # Parameters
    period = 10
    fast_ema = 2
    slow_ema = 30

    # Calculate AMA
    ama = adaptive_moving_average(data, period, fast_ema, slow_ema)

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(data, label='Price', alpha=0.7)
    plt.plot(ama, label='Adaptive Moving Average', color='orange')
    plt.legend()
    plt.title('Adaptive Moving Average Strategy')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()

if __name__ == "__main__":
    main()
