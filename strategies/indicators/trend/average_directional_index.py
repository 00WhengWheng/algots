import pandas as pd

def average_directional_index(high, low, close, period=14):
    """
    Calculate Average Directional Index (ADX).
    
    Args:
        high, low, close (list or pandas.Series): High, Low, and Close prices.
        period (int): Lookback period.
    
    Returns:
        pandas.Series: ADX values.
    """
    df = pd.DataFrame({'high': high, 'low': low, 'close': close})
    df['tr'] = df['high'] - df['low']
    df['+dm'] = df['high'].diff().clip(lower=0)
    df['-dm'] = df['low'].diff().clip(upper=0).abs()
    atr = df['tr'].rolling(window=period).mean()
    plus_di = (df['+dm'].rolling(window=period).sum() / atr) * 100
    minus_di = (df['-dm'].rolling(window=period).sum() / atr) * 100
    adx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    return adx.rolling(window=period).mean()
