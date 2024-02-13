import sys
import numpy as np
import pandas as pd
import math
from datetime import datetime
from moving_averages import weighted_moving_average_last
    
symbol = "BTC/USD"
_tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
_ohlc_cols = ['open', 'high', 'low', 'close']
_ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
_tma_cols = ['timestamp']+ _ma_cols
_all_cols = _tohlc_cols + _ma_cols
periods = {'open': 9, 'high': 5, 'low': 9, 'close': 5}

def add_bar_to_bars(bars, bar:dict):  
    bar_to_add = bar.copy()
    for i,attr in enumerate(_ohlc_cols):
        period = periods[attr]
        values = bars[attr].values
        if len(values) < period:
            bar_to_add[_ma_cols[i]] = np.nan
        else:
            try:
                bar_to_add[_ma_cols[i]] = weighted_moving_average_last(values, period)
            except Exception as e:
                print(e, flush=True)
                print(f"values: {values}, period: {period}", flush=True)
                sys.exit()
    n = len(bars)
    bars.loc[n] = bar_to_add
    return {'name': n, 'timestamp': bar_to_add['timestamp'], 'open': bar_to_add['open'], 'high': bar_to_add['high'], 'low': bar_to_add['low'], 'close': bar_to_add['close'], 'maopen': bar_to_add['maopen'], 'mahigh': bar_to_add['mahigh'], 'malow': bar_to_add['malow'], 'maclose': bar_to_add['maclose']}


def add_bar_to_habars(HAbars, bar):
    ha_close = (bar['open'] + bar['high'] + bar['low'] + bar['close']) / 4
    if len(HAbars) == 0:
        ha_open = (bar['open'] + bar['close']) / 2
    else:
        ha_open = (HAbars.iloc[-1]['open'] + HAbars.iloc[-1]['close']) / 2
    ha_high = max(bar['high'], ha_open, ha_close)
    ha_low = min(bar['low'], ha_open, ha_close)
    row = {'timestamp': bar['timestamp'], 'open': ha_open, 'high': ha_high, 'low': ha_low, 'close': ha_close}
    HAbars.loc[bar['name']] = row
    return {'name': bar['name'], 'timestamp': bar['timestamp'], 'open': ha_open, 'high': ha_high, 
            'low': ha_low, 'close': ha_close}

def add_bar_to_hamabars(HAMAbars, bar):
    if len(HAMAbars) == 0:
        hama_open = (bar['maopen'] + bar['maclose']) / 2
        hama_close = (bar['maopen'] + bar['mahigh'] + bar['malow'] + bar['maclose']) / 4
        hama_high = max(bar['mahigh'], hama_open, hama_close)
        hama_low = min(bar['malow'], hama_open, hama_close)
    else:
        hama_open = (HAMAbars.iloc[-1]['open'] + HAMAbars.iloc[-1]['close']) / 2
        hama_close = (bar['maopen'] + bar['mahigh'] + bar['malow'] + bar['maclose']) / 4
        hama_high = max(bar['mahigh'], hama_open, hama_close)
        hama_low = min(bar['malow'], hama_open, hama_close)
    row = {'timestamp': bar['timestamp'], 'open': hama_open, 'high': hama_high, 
           'low': hama_low, 'close': hama_close}
    HAMAbars.loc[bar['name']] = row
    

def update_barsN(bars_n, bars, grouping_N):
    subdf = bars.iloc[-grouping_N:].copy()
    t = subdf.timestamp.iloc[-1]
    o = subdf.open.iloc[0]
    c = subdf.close.iloc[-1]
    h = subdf.high.max()
    l = subdf.low.min()
    mao =subdf.maopen.iloc[0]
    mac = subdf.maclose.iloc[-1]
    mah = subdf.mahigh.max()
    mal = subdf.malow.min()
    row_dict = dict(zip( _all_cols, [t,o,h,l,c,mao,mah,mal,mac]))
    name = subdf.index[-1]
    n = len(bars) % grouping_N 
    # row_series = pd.Series(row_dict) 
    bars_n[n].loc[name] = row_dict
    return {'name': name, 'timestamp': t, 'open': o, 'high': h, 'low': l, 'close': c, 
            'maopen': mao, 'mahigh': mah, 'malow': mal, 'maclose': mac}

    
def analysis_process(queues):
    raw_bars_queue = queues['raw_bars']
    command_queue = queues['command']
    bars_queue = queues['bars']
    mabars_queue = queues['mabars']
    habars_queue = queues['ha_bars']
    hama_queue = queues['hama_bars']
    groupN_queue = queues['groupN']
    
    bars = pd.DataFrame(columns=_all_cols)
    grouping_N = 5
    bars_n = []
    for i in range(grouping_N):
        bars_n.append(pd.DataFrame(columns=_all_cols))
    HAbars = pd.DataFrame(columns=_tohlc_cols)
    HAMAbars = pd.DataFrame(columns=_tohlc_cols)
    bars_N_grouped = pd.DataFrame(columns=_all_cols)
        
    while True:
        while not command_queue.empty():
            command = command_queue.get()
            print("Received command:", command)
            if command == "get_info":
                response = "Some information you requested"
                bars_queue.put(response)

        while not raw_bars_queue.empty():
            bar = raw_bars_queue.get()
            bar_added_with_name= add_bar_to_bars(bars, bar)
            
            bars_queue.put(bar_added_with_name)
            mabars_queue.put(bar_added_with_name)
            
            habar_with_name = add_bar_to_habars(HAbars, bar_added_with_name)
            habars_queue.put(habar_with_name)
            
            hamabar_with_name = add_bar_to_hamabars(HAMAbars, bar_added_with_name)
            hama_queue.put(hamabar_with_name)
            
            # if len(bars) >= grouping_N:
            #     name, barN_added = update_barsN(bars_n, bars, grouping_N)
            #     bars_N_grouped.loc[name] = barN_added
