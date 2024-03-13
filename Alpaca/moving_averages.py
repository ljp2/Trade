import pandas as pd
import numpy as np

def dema_last(series, period):
    # Convert the series to a pandas Series if it's not already
    series = pd.Series(series)
    # Calculate the first EMA
    ema1 = series.ewm(span=period, adjust=False).mean()
    # Calculate the second EMA
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    # Calculate the DEMA
    dema = 2 * ema1 - ema2
    # Return the last value
    return dema.iloc[-1]

def simple_moving_average_last(values, period):
    if len(values) < period:
        return np.nan
    else:
        return sum(values[-period:]) / period
    
def weighted_moving_average_last(values, period):
    if len(values) < period:
        return None
    weights = list(range(1, period + 1))
    weighted_values = values[-period:]
    return sum(w*v for w, v in zip(weights, weighted_values)) / sum(weights)
