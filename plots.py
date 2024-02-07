import pyqtgraph as pg
from PyQt5 import QtGui
import numpy as np

class DynamicPlotter():
    def __init__(self, window_title=""):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title=window_title)
        self.plot = self.win.addPlot(title='Dynamic Plotting')
        self.curve = self.plot.plot(pen='y')
        self.data = np.array([])

    def update(self, new_data):
        self.data = np.append(self.data, new_data)
        self.curve.setData(self.data)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def close(self):
        self.app.quit()


# Usage
if __name__ == "__main__":
    plotter = DynamicPlotter("Dynamic Plotter")
    for i in range(100):
        plotter.update(np.random.rand())
    plotter.start()