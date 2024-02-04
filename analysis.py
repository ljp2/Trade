import sys
import numpy as np
import pandas as pd
import math

from moving_averages import weighted_moving_average_last
    
symbol = "BTC/USD"
_tohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
_ohlc_cols = ['open', 'high', 'low', 'close']
_ma_cols = ['maopen', 'mahigh', 'malow', 'maclose']
_tma_cols = ['timestamp']+ _ma_cols
_all_cols = _tohlc_cols + _ma_cols
periods = {'open': 9, 'high': 5, 'low': 9, 'close': 5}
grouping_N = 5


def add_bar_to_habars(HAbars, bars):
    new_bar = {attr:getattr(bars.iloc[-1], attr) for attr in _tohlc_cols}
    ha_close = (new_bar['open'] + new_bar['high'] + new_bar['low'] + new_bar['close']) / 4
    if len(HAbars) == 0:
        ha_open = (new_bar['open'] + new_bar['close']) / 2
    else:
        ha_open = (HAbars.iloc[-1]['open'] + HAbars.iloc[-1]['close']) / 2
    ha_high = max(new_bar['high'], ha_open, ha_close)
    ha_low = min(new_bar['low'], ha_open, ha_close)
    row = {'timestamp': new_bar['timestamp'], 'open': ha_open, 'high': ha_high, 'low': ha_low, 'close': ha_close}
    HAbars.loc[len(HAbars)] = row


def add_bar_to_hamabars(HAMAbars, bars):
    new_bar = {attr:getattr(bars.iloc[-1], attr) for attr in _tma_cols}
    
    if any(math.isnan(value) for value in new_bar.values()):
        hama_open = hama_high = hama_low = hama_close = np.nan
        
    elif HAMAbars.iloc[-1].isnull().any():
        hama_open = (new_bar['maopen'] + new_bar['maclose']) / 2
        hama_close = (new_bar['maopen'] + new_bar['mahigh'] + new_bar['malow'] + new_bar['maclose']) / 4
        hama_high = max(new_bar['mahigh'], hama_open, hama_close)
        hama_low = min(new_bar['malow'], hama_open, hama_close)
        
    else:
        hama_open = (HAMAbars.iloc[-1]['open'] + HAMAbars.iloc[-1]['close']) / 2
        hama_close = (new_bar['maopen'] + new_bar['mahigh'] + new_bar['malow'] + new_bar['maclose']) / 4
        hama_high = max(new_bar['mahigh'], hama_open, hama_close)
        hama_low = min(new_bar['malow'], hama_open, hama_close)
    row = {'timestamp': new_bar['timestamp'], 'open': hama_open, 'high': hama_high, 'low': hama_low, 'close': hama_close}
    HAMAbars.loc[len(HAMAbars)] = row
     
        
def add_row_to_bars(bars, new_bar):
    row = {attr:getattr(new_bar, attr) for attr in _tohlc_cols}
    row['timestamp'] = row['timestamp'].timestamp()
    for i,key in enumerate(_ohlc_cols):
        period = periods[key]
        values = bars[key].values
        if len(values) < period:
            row[_ma_cols[i]] = np.nan
        else:
            row[_ma_cols[i]] = weighted_moving_average_last(values, period)
    bars.loc[len(bars)] = row
    
def update_barsN(bars_n, bars):
    if len(bars) < grouping_N:
        return
    subdf = bars.iloc[-grouping_N:].copy()
    index = subdf.index[0]
    t = subdf.timestamp.iloc[0]
    o = subdf.open.iloc[0]
    c = subdf.close.iloc[-1]
    h = subdf.high.max()
    l = subdf.low.min()
    mao =subdf.maopen.iloc[0]
    mac = subdf.maclose.iloc[-1]
    mah = subdf.mahigh.max()
    mal = subdf.malow.min()
    row = [t,o,h,l,c,mao,mah,mal,mac]
    n = len(bars) % grouping_N     
    tf = bars_n[n]
    tf.loc[index] = row

def analysis_process(raw_bars_queue, analysis_queue, command_queue):
    
    bars = pd.DataFrame(columns=_all_cols)
    bars_n = []
    for i in range(grouping_N):
        bars_n.append(pd.DataFrame(columns=_all_cols))
    HAbars = pd.DataFrame(columns=_tohlc_cols)
    HAMAbars = pd.DataFrame(columns=_tohlc_cols)
        
    while True:
        # Check for incoming commands
        while not command_queue.empty():
            command = command_queue.get()
            print("Received command:", command)
            if command == "get_info":
                response = "Some information you requested"
                analysis_queue.put(response)

        # Receive data from the bars supplier
        if not raw_bars_queue.empty():
            data = raw_bars_queue.get()
            if data[0] == "init":
                print("Received init data:", flush=True)
                for bar in data[1]:
                    add_row_to_bars(bars, bar)
                    update_barsN(bars_n, bars)
                    add_bar_to_habars(HAbars, bars)
                    add_bar_to_hamabars(HAMAbars, bars)
                # print(bars.tail(), flush=True)
                # print('\nHAbars\n', HAbars.tail(3), flush=True)
                print('\nHAMAbars\n', HAMAbars.tail(3), flush=True)
                analysis_queue.put(bars.close.values)
                
            elif data[0] == "bar":
                add_row_to_bars(bars, bar)
                update_barsN(bars_n, bars)
                add_bar_to_habars(HAbars, bars)
                add_bar_to_hamabars(HAMAbars, bars)
                # print('\n', bars.tail(2), flush=True)
                # print('\nHAbars\n', HAbars.tail(2), flush=True)
                print('\nHAMAbars\n', HAMAbars.tail(2), flush=True)
                analysis_queue.put(bars.close.values)
            # Perform analysis on the received data

