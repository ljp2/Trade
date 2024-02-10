from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPicture
from PyQt6.QtCore import QRectF, QPointF
import pyqtgraph as pg
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
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        data = [  ## fields are (time, open, close, min, max).
            (1., 10, 13, 5, 15),
            (2., 13, 17, 9, 20),
            (3., 17, 14, 11, 23),
            (4., 14, 15, 5, 19),
            (5., 15, 9, 8, 22),
            (6., 9, 15, 8, 16),
        ]

        self.item = CandlestickItem(data)
        self.plot_widget.addItem(self.item)
        self.plot_widget.setXRange(1, 7)
        self.plot_widget.setYRange(4.5, 18)

        # Update the plot with new data
        new_data = (7., 15, 11, 10, 18)
        self.item.update_plot(new_data)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()