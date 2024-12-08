def parabolic_sar(high, low, acceleration_factor=0.02, max_acceleration=0.2):
    """
    Calculate Parabolic SAR.
    
    Args:
        high, low (list): High and Low prices.
        acceleration_factor (float): Step size.
        max_acceleration (float): Maximum step.
    
    Returns:
        list: SAR values.
    """
    sar = []
    trend = 1  # 1 for uptrend, -1 for downtrend
    af = acceleration_factor
    ep = high[0] if trend == 1 else low[0]
    sar.append(low[0] if trend == 1 else high[0])
    for i in range(1, len(high)):
        sar.append(sar[-1] + af * (ep - sar[-1]))
        if trend == 1:
            if high[i] > ep:
                ep = high[i]
                af = min(af + acceleration_factor, max_acceleration)
            if sar[-1] > low[i]:
                trend = -1
                ep = low[i]
                af = acceleration_factor
        else:
            if low[i] < ep:
                ep = low[i]
                af = min(af + acceleration_factor, max_acceleration)
            if sar[-1] < high[i]:
                trend = 1
                ep = high[i]
                af = acceleration_factor
    return sar
