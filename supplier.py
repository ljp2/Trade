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


def bars_supplier_process(raw_bars_queue):
    print("bars_process started", flush=True)
    
    client = CryptoHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    request = CryptoLatestBarRequest(symbol_or_symbols="BTC/USD")

    # get historical bars to initialize the bars dataframe
    end = datetime.utcnow()
    start = end - timedelta(hours=1)
    bars = getHistoricalCryptoBars("BTC/USD", start, end)
    raw_bars_queue.put(("init", bars))

    last_timestamp = bars[-1].timestamp.timestamp()
    i = 1
    while True:
        try:
            print(f"t{i}", end=" ", flush=True)
            i += 1
            bar = client.get_crypto_latest_bar(request_params=request)["BTC/USD"]
            if bar.timestamp.timestamp() == last_timestamp:
                sleep(5)
                continue
            else:
                raw_bars_queue.put(("bar", bar))
                last_timestamp = bar.timestamp.timestamp()
                i = 0
                sleep(55)
        except Exception as e:
            print(e,flush=True)
            sleep(3)

