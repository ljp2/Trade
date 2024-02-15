from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QPicture
import pyqtgraph as pg
import numpy as np
from multiprocessing import Queue

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
    def __init__(self, data_queue=None, title = "Candles"):
        super().__init__()
        self.data_queue = data_queue
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget(title=title)
        self.layout.addWidget(self.plot_widget)
        self.rw = 0.6
        self.rw2 = self.rw / 2
        
        self.line_x = []
        self.line_y = []
        self.line = self.plot_widget.plot(self.line_x, self.line_y, pen=pg.mkPen(color='w', width=2))  
        
        # Set up a timer to periodically check for new data
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every 1 second

    def plot_candle(self, n,o,h,l,c):
        color = 'g' if c>o else 'r' if c<o else 'y'
        pen = pg.mkPen(color=color, width=2)
        wick = ((n, n), (l, h))
        self.plot_widget.plot(*wick, pen=pen)
        
        rect =((n - self.rw2, min(o,c)), (self.rw, abs(o - c)))
        rect_item = FillableRect(rect, color)
        self.plot_widget.addItem(rect_item)
        
    
    def candle_from_bar(self, bar):
            nohlc = [
                bar['name'],
                bar['open'],
                bar['high'],
                bar['low'],
                bar['close']
            ]
            return nohlc
    
        
    def update_plot(self):
        def plot_bar(bar):
            n,o,h,l,c = self.candle_from_bar(bar)
            self.plot_candle(n,o,h,l,c)
            self.line_x.append(n)
            self.line_y.append(c)
            self.line.setData(self.line_x, self.line_y)
            
            
        while not self.data_queue.empty():
            data = self.data_queue.get()
            plot_bar(data)
            
        
    def clear_plot(self):
        self.plot_widget.clear()

class PlotMaCandles(PlotCandles):
    def __init__(self, data_queue=None, title = None):
        super().__init__(data_queue, title)

    def candle_from_bar(self, bar):
        try:
            nohlc = (
                bar['name'],
                bar['maopen'],
                bar['mahigh'],
                bar['malow'],
                bar['maclose']
            )
            return nohlc    
        except Exception as e:
            print(e, flush=True)

        
class PlotHACandles(PlotCandles):
    def __init__(self, data_queue=None, title = 'HA Candles'):
        super().__init__(data_queue, title)

    def candle_from_bar(self, bar):
        try:
            nohlc = (
                bar['name'],
                bar['haopen'],
                bar['hahigh'],
                bar['halow'],
                bar['haclose']
            )
            return nohlc    
        except Exception as e:
            print(e, flush=True)

        

class PlotHAMACandles(PlotCandles):
    def __init__(self, data_queue=None, title = 'HAMA Candles'):
        super().__init__(data_queue, title)

    def candle_from_bar(self, bar):
        try:
            nohlc = (
                bar['name'],
                bar['hamaopen'],
                bar['hamahigh'],
                bar['hamalow'],
                bar['hamaclose']
            )
            return nohlc    
        except Exception as e:
            print(e, flush=True)

        

class PlotGroupN(PlotCandles):
    def __init__(self, data_queue=None, title = None):
        super().__init__(data_queue, title)

    def candle_from_bar(self, bar):
        try:
            nohlc = (
                bar['name'],
                bar['open'],
                bar['high'],
                bar['low'],
                bar['close']
            )
            return nohlc    
        except Exception as e:
            print(e, flush=True)