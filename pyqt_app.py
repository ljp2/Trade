from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QPicture
from PyQt6.QtCore import QRectF, QPointF

import pyqtgraph as pg
from multiprocessing import Queue
import numpy as np


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        # w_rect = (self.data[1][0] - self.data[0][0]) / 3.  # width for the rectangles
        w_rect = 0.3
        for (t, open, close, min, max) in self.data:
            if open > close:
                p.setPen(QPen(QColor(255, 0, 0), .05))  # red pen with width 2
                p.setBrush(QBrush(QColor(255, 0, 0)))  # red
            else:
                p.setPen(QPen(QColor(0, 255, 0), .05))  # green pen with width 2
                p.setBrush(QBrush(QColor(0, 255, 0)))  # green
            p.drawLine(QPointF(t, min), QPointF(t, max))
            p.drawRect(QRectF(t-w_rect, open, w_rect*2, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

    def update_plot(self, new_data):
        self.data.append(new_data)
        self.generatePicture()
        self.update()

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
            y = [float(x) for x in data.close.values]
            self.plot_widget.plot(y)
