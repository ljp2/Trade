from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QPicture
import pyqtgraph as pg
import numpy as np
from multiprocessing import Queue

# from plots import PlotCandles

class MainWindow(QMainWindow):
    def __init__(self, queues):
        super().__init__()
        self.data_queue = queues['analysis']
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQtGraph with Multiprocessing")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # self.plot_widget = PlotCandles(self.data_queue)
        # layout.addWidget(self.plot_widget)

        # # Set up a timer to periodically check for new data
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start(1000)  # Update every 1 second

    # def update_plot(self):
    #     while not self.data_queue.empty():
    #         bar = self.data_queue.get()
            
    #         tohlc = (
    #             bar['cnt'],
    #             bar['open'],
    #             bar['high'],
    #             bar['low'],
    #             bar['close']
    #         )
            
    #         print(tohlc)
            
    #         self.plot_widget.plot_candle(tohlc)
            
            
            
# if __name__ == '__main__':
#     app = QApplication([])
#     data_queue = Queue()
#     main = MainWindow(data_queue)
#     main.show()
    
#     main.plot_widget.update_plot((1, 10, 13, 5, 7))
    
#     timer = QTimer()
#     # timer.singleShot(2000, lambda: main.plot_widget.clear_plot())
#     timer.singleShot(2000, lambda: data_queue.put((2, 7, 17, 5, 15)))

#     app.exec()