import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter, QPicture
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
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.setPen(pg.mkPen('w'))
            p.drawLine(QPointF(t, min), QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QRectF(t-w, open, w*2, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

app = QApplication(sys.argv)
data = [  ## fields are (time, open, close, min, max).
    (1., 10, 13, 5, 15),
    (2., 13, 17, 9, 20),
    (3., 17, 14, 11, 23),
    (4., 14, 15, 5, 19),
    (5., 15, 9, 8, 22),
    (6., 9, 15, 8, 16),
]
item = CandlestickItem(data)
plt = pg.plot()
plt.addItem(item)
plt.setXRange(1, 6)
plt.setYRange(4, 24)

if __name__ == '__main__':
    sys.exit(app.exec())