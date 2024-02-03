from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from multiprocessing import Queue

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
        # Check if there's new data in the queue
        while not self.data_queue.empty():
            data = self.data_queue.get()
            # Update the plot with the new data
            self.plot_widget.plot(data)
