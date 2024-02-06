from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from multiprocessing import Queue
import numpy as np

def filter_numeric(arr):
    numeric_values = []
    for element in arr:
        try:
            numeric_values.append(float(element))
        except ValueError:
            continue
    return np.array(numeric_values)

class MainWindow(QMainWindow):
    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQtGraph with Multiprocessing")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Set up a timer to periodically check for new data
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every 1 second

    def update_plot(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            print(type(data.close.values))  # print the type of data.close.values
            print(type(data.close.values[0]))  # print the type of the first element in data.close.values
            print('flags', data.close.values.flags)

            y = [float(x) for x in data.close.values]
            print(type(y))  # print the type of y
            print(type(y[0]))  # print the type of the first element in y

            # try:
            #     y = [float(x) for x in data.close.values]
            #     print('isfinite', np.isfinite(y), flush=True)
            # except Exception as e:
            #     print('data.close.values\n', data.close.values, flush=True)
            #     print('error', flush=True)
            #     print(e, flush=True)
                
            # y = filter_numeric(data.close.values)
            # print(type(y), flush=True)
            # print('isfinite', np.isfinite(y), flush=True)
            # print(y)
            # self.plot_widget.plot(y)

            

# if __name__ == "__main__":
#     app = QApplication([])
#     data_queue = Queue()
#     data_queue.put(1)
#     window = MainWindow(data_queue)
#     window.show()
#     app.exec()
            # data = [43170.05,43209.5195,43207.725,43239.488,43235.95,43224.95,43211.45,
            #     43233.9,43218.643,43227.86,43212.151,43232.998,43159.8085,43132.822]
            # Update the plot with the new data
            
            # print(np.isfinite(data.close), flush=True)