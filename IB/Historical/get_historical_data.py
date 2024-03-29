from ibapi.client import *
from ibapi.wrapper import *
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
import queue


class TestApp(EClient, EWrapper):
    def __init__(self, day:str):
        EClient.__init__(self, self)
        self.end_day = day.strftime("%Y%m%d 23:59:00 US/Eastern")
        self.filename = day.strftime("%Y%m%d.csv")
        self.data_file = open(self.filename, 'w')


    def nextValidId(self, orderId: int):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        self.reqHistoricalData(orderId, contract, self.end_day, "1 D", "1 hour", "TRADES", 0, 1, 0, [])

    def historicalData(self, reqId, bar):
        s = f"{bar.date}\t{bar.open}\t{bar.high}\t{bar.low}\t{bar.close}\t{bar.volume}"
        self.data_file.write(s + '\n')
        
    def historicalDataEnd(self, reqId, start, end):
        print(f"End of HistoricalData {self.filename}")
        self.data_file.close()
        self.disconnect()

def run_app_process(day:str):
    app = TestApp(day)
    app.connect("127.0.0.1", 4002, 1000)
    app.run()    


def get_weekdays(start_date, end_date):
    weekdays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
            weekdays.append(current_date)
        current_date += timedelta(days=1)
    return weekdays

if __name__ == '__main__':
    start_date = datetime(2024, 3, 7)
    end_date = datetime(2024, 3, 12)
    weekday_list = get_weekdays(start_date, end_date)
    for day in weekday_list:
        app_process = Process(target=run_app_process, args=(day,), daemon=True)
        app_process.start()
        app_process.join()
        print(f"Process {day} finished")
        break
