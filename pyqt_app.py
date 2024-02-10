from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QPicture
import pyqtgraph as pg
import numpy as np

class FillableRect(pg.GraphicsObject):
    def __init__(self, rect, color):
        pg.GraphicsObject.__init__(self)
        self.rect = rect
        self.color = color
        self.generatePicture()

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        p.setPen(pg.mkPen(self.color))
        p.setBrush(pg.mkBrush(self.color))
        p.drawRect(QRectF(self.rect[0][0], self.rect[0][1], self.rect[1][0], self.rect[1][1]))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

class PlotCandles(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.rw = 0.6
        self.rw2 = self.rw / 2

    def plot_candle(self, tohlc):
        print(tohlc)
        t,o,h,l,c = tohlc
        color = 'g' if c>o else 'r' if c<o else 'y'
        pen = pg.mkPen(color=color, width=2)
        line = ((t, t), (l, h))
        self.plot_widget.plot(*line, pen=pen)
        
        rect =((t - self.rw2, min(o,c)), (self.rw, abs(o - c)))
        rect_item = FillableRect(rect, color)
        self.plot_widget.addItem(rect_item)
        
    def plot_data(self, data, shape):
        if shape == 'line':
            self.plot_widget.plot(data, pen=pg.mkPen(color=(np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), width=2))
        elif shape == 'rectangle':
            for rect in data:
                color = (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
                rect_item = FillableRect(rect, color)
                self.plot_widget.addItem(rect_item)

    def update_plot(self, new_data, shape):
        self.plot_data(new_data, shape)
        
    def clear_plot(self):
        self.plot_widget.clear()
                
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot_widget = PlotCandles(self)
        self.setCentralWidget(self.plot_widget)

if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()
    
    main.plot_widget.plot_candle((1, 10, 13, 5, 7))
    
    timer = QTimer()
    # timer.singleShot(2000, lambda: main.plot_widget.clear_plot())
    timer.singleShot(2000, lambda: main.plot_widget.plot_candle((2, 7, 17, 5, 15)))

    app.exec()