def ichimoku_cloud(high, low, close, period1=9, period2=26, period3=52):
    """
    Calculate Ichimoku Cloud components.

    Args:
        high, low, close (list or pandas.Series): High, Low, and Close prices.
        period1, period2, period3 (int): Lookback periods for components.
    
    Returns:
        dict: Ichimoku components (tenkan-sen, kijun-sen, senkou span A, senkou span B, chikou span).
    """
    tenkan_sen = (high.rolling(window=period1).max() + low.rolling(window=period1).min()) / 2
    kijun_sen = (high.rolling(window=period2).max() + low.rolling(window=period2).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(period2)
    senkou_span_b = ((high.rolling(window=period3).max() + low.rolling(window=period3).min()) / 2).shift(period2)
    chikou_span = close.shift(-period2)
    return {
        "tenkan_sen": tenkan_sen,
        "kijun_sen": kijun_sen,
        "senkou_span_a": senkou_span_a,
        "senkou_span_b": senkou_span_b,
        "chikou_span": chikou_span
    }
