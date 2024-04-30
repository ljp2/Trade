import os
from datetime import datetime, timedelta
from threading import Thread, Event
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

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
        
    def historicalDataEnd(self, reqId, start, end):
        self.done.set()


def run_loop(app):
    app.run()
    
def get_historical_data(app, contract, endDateTime):
    duration = int(6.5 * 60 * 60)
    durationStr = f"{duration} S"
    bar_size = "1 min"
    whatToShow = "TRADES"
    useRTH = 0
    formatDate = 1
    keepUpToDate = False
    app.done.clear()
    app.data.clear()
    app.reqHistoricalData(4002, contract, endDateTime, duration, bar_size, 
                            whatToShow, useRTH, formatDate, keepUpToDate, [])
    app.done.wait()

def write_to_csv(data, filename):
    with open(filename, "w") as f:
        for bar in data:
            f.write(f"{bar.date[9:14]}\t{bar.open}\t{bar.high}\t{bar.low}\t{bar.close}\t{bar.volume}\n")

def main(data_directory: str):
    contract = Contract()
    contract.symbol = "SPY"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    app = HistDataApp()
    app.connect("127.0.0.1", 4002, clientId=0)
    api_thread = Thread(target=run_loop, args=(app,), daemon=True)
    api_thread.start()
    app.connection_ready.wait(5)

    current_data_files = os.listdir(data_directory)
    day = datetime.now() - timedelta(days=1)
    desired_days = 250
    n = 0
    while n < desired_days:
        if day.weekday() < 5:
            ymd = day.strftime("%Y%m%d")
            filename = f"{ymd}.csv"
            if filename in current_data_files:
                break
            endDateTime = ymd + " 16:00:00 US/Eastern"

            get_historical_data(app, contract, endDateTime)
            if ymd == app.data[0].date.split(" ")[0]:
                write_to_csv(app.data, f"{data_directory}/{filename}")
                print(ymd)
                n += 1
            else:
                print(f"Data for {ymd} is not available")
        day -= timedelta(days=1)
        time.sleep(15)
    app.disconnect()
    print("Done")


if __name__ == "__main__":
    data_directory = "C:/Data"
    main(data_directory)