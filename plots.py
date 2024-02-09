import sys
import multiprocessing
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.queue = multiprocessing.Queue()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.plot_item = self.plot_widget.plotItem
        self.curve1 = self.plot_item.plot()
        self.curve2 = self.plot_item.plot()

        self.data1 = []
        self.data2 = []

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every second

    def update_plot(self):
        while not self.queue.empty():
            data = self.queue.get()
            if len(data) == 2:
                x, y1, y2 = data
                self.data1.extend(y1)
                self.data2.extend(y2)

        if self.data1:
            self.curve1.setData(self.data1)
        if self.data2:
            self.curve2.setData(self.data2)

