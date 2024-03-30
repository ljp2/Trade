from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *
from datetime import datetime, timedelta

from threading import Thread, Event
import time


class HistDataApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.done = Event()  # use threading.Event to signal between threads
        self.connection_ready = Event()  # to signal the connection has been established
        self.done.clear()
        self.connection_ready.clear()

    def nextValidId(self, orderId: int):
        print(f"Connection ready, next valid order ID: {orderId}")
        self.connection_ready.set()  # signal that the connection is ready
          
    def historicalData(self, reqId, bar):
        self.data.append(bar)
        print(f"{bar.date} {bar.open} {bar.high} {bar.low} {bar.close} {bar.volume}")
        
    def historicalDataEnd(self, reqId, start, end):
        self.done.set()


def get_weekdays(start_date, end_date):
    weekdays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
            weekdays.append(current_date)
        current_date += timedelta(days=1)
    return weekdays

def run_loop(app):
    app.run()
    
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
    
app = HistDataApp()
app.connect("127.0.0.1", 4002, clientId=0)
api_thread = Thread(target=run_loop, args=(app,), daemon=True)
api_thread.start()
app.connection_ready.wait()


app.reqHistoricalData(4002, contract, "", "1 D", "1 hour", "TRADES", 0, 1, 0, [])
app.done.wait()


for bar in app.data:
    print(f"{bar.date} {bar.open} {bar.high} {bar.low} {bar.close} {bar.volume}")


# app.data_file = open("AAPL_1D.csv", "w")

app.disconnect()