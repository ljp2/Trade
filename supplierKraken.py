import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from math import sqrt
import requests

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
    
    X = []
    ix = 0
    since = int(time.time() - 60*60*prefetch_hours )
    url = f'https://api.kraken.com/0/public/OHLC?pair=XBTUSD&since={since}&interval=1&token=1&nonce'
    resp = requests.get(url).json()
    bars = resp['result']['XXBTZUSD']
    cols = ['timestamp', 'open', 'high', 'low', 'close']
    
    for bar in bars:
        bar_dict = {
            'timestamp': int(bar[0]) ,
            'open': float(bar[1]),
            'high': float(bar[2]),
            'low': float(bar[3]),
            'close': float(bar[4])
        }
        raw_bars_queue.put(bar_dict)
    last_timestamp = bar_dict['timestamp']
        
    i = 0
    while True:
        try:
            time.sleep(55)
            # print(f"t{i}", end=" ", flush=True)
            # i += 1
            # bar = client.get_crypto_latest_bar(request_params=request)["BTC/USD"]
            # if bar.timestamp == last_timestamp:
            #     time.sleep(5)
            #     continue
            # else:
            #     last_timestamp = bar.timestamp
            #     bar_dict = {'timestamp': bar.timestamp, 'open': bar.open, 'high': bar.high, 'low': bar.low,'close': bar.close }
            #     raw_bars_queue.put(bar_dict)
            #     i = 0
            #     time.sleep(55)
        except Exception as e:
            print(e,flush=True)
            time.sleep(3)

