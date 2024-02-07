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

def add_bar_to_bars(bars, bar:pd.Series):  
    row = {attr:bar[attr] for attr in _tohlc_cols}
    for i,attr in enumerate(_ohlc_cols):
        period = periods[attr]
        values = bars[attr].values
        if len(values) < period:
            row[_ma_cols[i]] = np.nan
        else:
            row[_ma_cols[i]] = weighted_moving_average_last(values, period)
    row_series = pd.Series(row, name=bar.name)
    bars.loc[bar.name] = row_series
    return row_series
    
def add_bar_to_barsN(bars_n, bars, grouping_N):
    if len(bars) < grouping_N:
        return None
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
    row_to_add = pd.Series(row_dict, name = subdf.index[-1])
    n = len(bars) % grouping_N     
    bars_n[n].loc[row_to_add.name] = row_to_add
    return row_to_add

    
def add_bar_to_bars_grouped(bars_grouped, barN_added):
    if barN_added is None:
        return
    # print(barN_added.name, barN_added.timestamp, barN_added.close, flush=True)
    bars_grouped.loc[barN_added.name] = barN_added


def add_bar_to_habars(HAbars, bar):
    ha_close = (bar['open'] + bar['high'] + bar['low'] + bar['close']) / 4
    if len(HAbars) == 0:
        ha_open = (bar['open'] + bar['close']) / 2
    else:
        ha_open = (HAbars.iloc[-1]['open'] + HAbars.iloc[-1]['close']) / 2
    ha_high = max(bar['high'], ha_open, ha_close)
    ha_low = min(bar['low'], ha_open, ha_close)
    row = {'timestamp': bar['timestamp'], 'open': ha_open, 'high': ha_high, 'low': ha_low, 'close': ha_close}
    HAbars.loc[bar.name] = row


def add_bar_to_hamabars(HAMAbars, bar):
    if bar.isnull().any():
        hama_open = hama_high = hama_low = hama_close = np.nan
    elif HAMAbars.iloc[-1].isnull().any():
        hama_open = (bar['maopen'] + bar['maclose']) / 2
        hama_close = (bar['maopen'] + bar['mahigh'] + bar['malow'] + bar['maclose']) / 4
        hama_high = max(bar['mahigh'], hama_open, hama_close)
        hama_low = min(bar['malow'], hama_open, hama_close)
    else:
        hama_open = (HAMAbars.iloc[-1]['open'] + HAMAbars.iloc[-1]['close']) / 2
        hama_close = (bar['maopen'] + bar['mahigh'] + bar['malow'] + bar['maclose']) / 4
        hama_high = max(bar['mahigh'], hama_open, hama_close)
        hama_low = min(bar['malow'], hama_open, hama_close)
    row = {'timestamp': bar['timestamp'], 'open': hama_open, 'high': hama_high, 'low': hama_low, 'close': hama_close}
    HAMAbars.loc[bar.name] = row
        
    
def analysis_process(queues):
    raw_bars_queue = queues['raw_bars']
    command_queue = queues['command']
    analysis_queue = queues['analysis']
    
    bars = pd.DataFrame(columns=_all_cols)
    grouping_N = 5
    bars_n = []
    for i in range(grouping_N):
        bars_n.append(pd.DataFrame(columns=_all_cols))
    HAbars = pd.DataFrame(columns=_tohlc_cols)
    HAMAbars = pd.DataFrame(columns=_tohlc_cols)
    bars_grouped = pd.DataFrame(columns=_all_cols)
        
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
                for index, bar in data[1].iterrows():
                    bar_added = add_bar_to_bars(bars, bar)
                    add_bar_to_habars(HAbars, bar_added)
                    add_bar_to_hamabars(HAMAbars, bar_added)
                    
                    barN_added = add_bar_to_barsN(bars_n, bars, grouping_N)
                    add_bar_to_bars_grouped(bars_grouped, barN_added)
                # print(bars.tail(), flush=True)
                # print('\nHAbars\n', HAbars.tail(3), flush=True)
                # print('\nHAMAbars\n', HAMAbars.tail(3), flush=True)
                # print(HAMAbars.tail(3), flush=True)
                analysis_queue.put(bars)
                
            elif data[0] == "bar":
                print("Received bar data:", flush=True)
                bar_added = add_bar_to_bars(bars, data[1])
                add_bar_to_habars(HAbars, bar_added)
                add_bar_to_hamabars(HAMAbars, bar_added)
                
                add_bar_to_bars_grouped(bars_grouped, barN_added)
                barN_added = add_bar_to_barsN(bars_n, bars, grouping_N)
                
                # print('\n', bars.tail(2), flush=True)
                # print('\nHAbars\n', HAbars.tail(2), flush=True)
                # print('\nHAMAbars\n', HAMAbars.tail(2), flush=True)
                # print(HAMAbars.tail(3), flush=True)
                analysis_queue.put(bars)
        
                
            # Perform analysis on the received data

