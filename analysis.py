import sys
import numpy as np
import pandas as pd
import math
from datetime import datetime
from time import sleep
from moving_averages import weighted_moving_average_last
    
symbol = "BTC/USD"
_ntohlc_cols = ['name', 'timestamp', 'open', 'high', 'low', 'close']
_ohlc_cols = ['open', 'high', 'low', 'close']
_ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
_tma_cols = ['timestamp']+ _ma_cols
_ha_cols = ['haopen', 'hahigh', 'halow', 'haclose']
_hama_cols = ['hamaopen', 'hamahigh', 'hamalow', 'hamaclose']

_all_cols = _ntohlc_cols + _ma_cols + _ha_cols + _hama_cols

periods = {'open': 9, 'high': 5, 'low': 9, 'close': 5}

def check_no_nan_values(dictionary, keys):
    for key in keys:
        if key in dictionary and math.isnan(dictionary[key]):
            return False
    return True

def add_ma_cols(input_bar, bars):
    bar = input_bar.copy()
    for i,attr in enumerate(_ohlc_cols):
        period = periods[attr]
        values = bars[attr].values
        if len(values) < period:
            bar[_ma_cols[i]] = np.nan
        else:
            try:
                bar[_ma_cols[i]] = weighted_moving_average_last(values, period)
            except Exception as e:
                print(e, flush=True)
                print(f"values: {values}, period: {period}", flush=True)
                sys.exit()
    return bar

def add_ha_cols(input_bar, bars):
    bar = input_bar.copy()
    ha_close = (bar['open'] + bar['high'] + bar['low'] + bar['close']) / 4
    if len(bars) == 0:
        ha_open = (bar['open'] + bar['close']) / 2
    else:
        ha_open = (bars.iloc[-1]['open'] + bars.iloc[-1]['close']) / 2
    ha_high = max(bar['high'], ha_open, ha_close)
    ha_low = min(bar['low'], ha_open, ha_close)
    bar['haopen'] = ha_open
    bar['hahigh'] = ha_high
    bar['halow'] = ha_low
    bar['haclose'] = ha_close
    return bar

def add_hama_cols(input_bar, bars):
    bar = input_bar.copy()
    if check_no_nan_values(bar, _ma_cols):
        if bars.iloc[-1].maopen == np.nan:
            hama_open = (bar['maopen'] + bar['maclose']) / 2
            hama_close = (bar['maopen'] + bar['mahigh'] + bar['malow'] + bar['maclose']) / 4
            hama_high = max(bar['mahigh'], hama_open, hama_close)
            hama_low = min(bar['malow'], hama_open, hama_close)
        else:
            hama_open = (bars.iloc[-1]['open'] + bars.iloc[-1]['close']) / 2
            hama_close = (bar['maopen'] + bar['mahigh'] + bar['malow'] + bar['maclose']) / 4
            hama_high = max(bar['mahigh'], hama_open, hama_close)
            hama_low = min(bar['malow'], hama_open, hama_close)
        bar['hamaopen'] = hama_open
        bar['hamahigh'] = hama_high
        bar['hamalow'] = hama_low
        bar['hamaclose'] = hama_close
    else:
        bar['hamaopen'] = np.nan
        bar['hamahigh'] = np.nan
        bar['hamalow'] = np.nan
        bar['hamaclose'] = np.nan
    return bar
        

def update_barsN(bars_n, bars, grouping_N):
    subdf = bars.iloc[-grouping_N:].copy()
    name = subdf.name.iloc[-1]
    t = subdf.timestamp.iloc[-1]
    o = subdf.open.iloc[0]
    c = subdf.close.iloc[-1]
    h = subdf.high.max()
    l = subdf.low.min()
    mao =subdf.maopen.iloc[0]
    mac = subdf.maclose.iloc[-1]
    mah = subdf.mahigh.max()
    mal = subdf.malow.min()
    
    n = len(bars) % grouping_N 
    row = dict(zip( _all_cols, [t,o,h,l,c,mao,mah,mal,mac]))
    bars_n[n].loc[name] = row
    
    return n, row
    
def analysis_process(queues):
    raw_bars_queue = queues['raw_bars']
    command_queue = queues['command']
    bars_queue = queues['bars']
    groupN_queue = queues['groupN']
    
    bars = pd.DataFrame(columns=_all_cols)
    grouping_N = 5
    bars_n = []
    for i in range(grouping_N):
        bars_n.append(pd.DataFrame(columns=_all_cols))
    bars_N_grouped = pd.DataFrame(columns=_all_cols)
        
    while True:
        while not command_queue.empty():
            command = command_queue.get()
            if command == "get_info":
                response = "Some information you requested"
                bars_queue.put(response)

        while not raw_bars_queue.empty():
            bar = raw_bars_queue.get()
            bar = add_ma_cols(bar, bars)
            # bar = add_ha_cols(bar, bars)
            # bar = add_hama_cols(bar, bars)
            name = len(bars)
            bar['name'] = name
            bars.loc[name] = bar
            
            queues['bars'].put(bar)
            
            if check_no_nan_values(bar, _ma_cols):
                queues['mabars'].put(bar)
                
            # queues['ha'].put(bar)
            
            # queues['hama'].put(bar)

            # if len(bars) >= grouping_N:
            #     n, row_added = update_barsN(bars_n, bars, grouping_N)
            #     bars_N_grouped.loc[name] = barN_added
            #     barN_added['name'] = name
            #     groupN_queue.put(barN_added)
