import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep
from math import sqrt

import alpaca.data.models as alpaca_models
from alpaca_api import getHistoricalCryptoBars
from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestBarRequest

from moving_averages import weighted_moving_average_last

from keys import paper_apikey, paper_secretkey
ALPACA_API_KEY = paper_apikey
ALPACA_SECRET_KEY = paper_secretkey


def bars_supplier_process(queues, prefetch_hours=1):
    raw_bars_queue = queues['raw_bars']
    client = CryptoHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    request = CryptoLatestBarRequest(symbol_or_symbols="BTC/USD")

    # get historical bars to initialize the bars dataframe
    end = datetime.utcnow()
    start = end - timedelta(hours=prefetch_hours)
    barset = getHistoricalCryptoBars("BTC/USD", start, end) 
    for bar in barset:
        bar_dict = {'timestamp': bar.timestamp, 'open': bar.open, 'high': bar.high, 'low': bar.low,'close': bar.close }   
        raw_bars_queue.put(bar_dict)
    last_timestamp = barset[-1].timestamp
        
    i = 0
    while True:
        try:
            print(f"t{i}", end=" ", flush=True)
            i += 1
            bar = client.get_crypto_latest_bar(request_params=request)["BTC/USD"]
            if bar.timestamp == last_timestamp:
                sleep(5)
                continue
            else:
                last_timestamp = bar.timestamp
                bar_dict = {'timestamp': bar.timestamp, 'open': bar.open, 'high': bar.high, 'low': bar.low,'close': bar.close }
                raw_bars_queue.put(bar_dict)
                i = 0
                sleep(55)
        except Exception as e:
            print(e,flush=True)
            sleep(3)

