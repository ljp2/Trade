import asyncio
import multiprocessing
from supplier import bars_supplier_process
from analysis import analysis_process
from pyqt_app import MainWindow
from PyQt6.QtWidgets import QApplication

from plots import PlotCandles, PlotMaCandles

def main():
    app = QApplication([])
    raw_bars_queue = multiprocessing.Queue()
    command_queue = multiprocessing.Queue()
    bars_queue = multiprocessing.Queue()
    mabars_queue = multiprocessing.Queue()
    habars_queue = multiprocessing.Queue()
    hama_queue = multiprocessing.Queue()
    groupN_queue = multiprocessing.Queue()
 
    queues = {'raw_bars': raw_bars_queue, 'bars': bars_queue, 'command': command_queue,
              'mabars': mabars_queue,  'ha_bars': habars_queue, 'hama_bars': hama_queue, 
              'groupN': groupN_queue }
    
    # Start the data receiver process
    receiver_process = multiprocessing.Process(
        target=analysis_process,
        args=(queues,),
        daemon=True
    )
    receiver_process.start()

    # Start the data supplier process
    supplier_process = multiprocessing.Process(
        target=bars_supplier_process,
        args=(queues,),
        daemon=True
    )
    supplier_process.start()
    



    groupN_plot = PlotCandles(data_queue=groupN_queue, title="Group N Bars")
    groupN_plot.show()    
        
    window = MainWindow(queues)
    window.show()

    # Start the application event loop
    app.exec()

if __name__ == "__main__":
    main()
