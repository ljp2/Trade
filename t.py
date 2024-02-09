from PyQt6.QtGui import QPainter, QPicture
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  # data must be list of tuples (time, open, high, low, close)
        self.generatePicture()

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        # draw candlesticks
        for (t, open, high, low, close) in self.data:
            p.drawLine(QPointF(t, high), QPointF(t, low))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QRectF(t-0.3, open, 0.6, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

    def update(self, new_candle):
        self.data.append(new_candle)
        self.generatePicture()

# Example usage:
app = QApplication([])

data = [ (1, 10, 15, 5, 13), (2, 13, 20, 12, 15), (3, 15, 22, 10, 20) ]
candlestick = CandlestickItem(data)

win = pg.GraphicsLayoutWidget()
plt = win.addPlot(title="Candlestick chart")
plt.addItem(candlestick)

# Add a new candle
candlestick.update((4, 20, 23, 15, 22))

win.show()

app.exec()