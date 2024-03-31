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
        # print(f"{bar.date} {bar.open} {bar.high} {bar.low} {bar.close} {bar.volume}")
        
    def historicalDataEnd(self, reqId, start, end):
        self.done.set()


def run_loop(app):
    app.run()
    
def get_historical_data(app, contract, end_date, duration="1 D", bar_size="1 min"):
    app.reqHistoricalData(4002, contract, end_date, duration, bar_size, "TRADES", 0, 1, 0, [])
    app.done.wait()

def write_to_csv(data, filename):
    with open(filename, "w") as f:
        for bar in data:
            f.write(f"{bar.date[9:14]}\t{bar.open}\t{bar.high}\t{bar.low}\t{bar.close}\n")

contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

app = HistDataApp()
app.connect("127.0.0.1", 4002, clientId=0)
api_thread = Thread(target=run_loop, args=(app,), daemon=True)
api_thread.start()
app.connection_ready.wait(5)

day = datetime.today() 
desired_days = 2
n = 0
while n < desired_days:
    if day.weekday() < 5:
        end_day_time =  day.strftime("%Y%m%d %H:%M:%S") + " US/Eastern"
        ymd = end_day_time.split(" ")[0]
        get_historical_data(app, contract, end_day_time)
        if ymd == app.data[0].date.split(" ")[0]:
            write_to_csv(app.data, f"{contract.symbol}_{ymd}.csv")
            n += 1
        else:
            print(f"Data for {ymd} is not available")
    day -= timedelta(days=1)
