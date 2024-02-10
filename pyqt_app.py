from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

    def plot_data(self, data, shape):
        if shape == 'line':
            self.plot_widget.plot(data, pen=pg.mkPen(color=(np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), width=2))
        elif shape == 'rectangle':
            for rect in data:
                self.plot_widget.addItem(pg.RectROI(rect[0], rect[1], pen=pg.mkPen(color=(np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), width=2)))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot_widget = PlotWidget(self)
        self.setCentralWidget(self.plot_widget)

if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()

    # Plot line
    line_data = np.random.normal(size=100)
    main.plot_widget.plot_data(line_data, 'line')

    # Plot rectangles
    rect_data = [((i, i), (1, 1)) for i in range(10)]
    main.plot_widget.plot_data(rect_data, 'rectangle')

    app.exec()