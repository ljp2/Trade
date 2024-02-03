import asyncio
import multiprocessing
from supplier import bars_supplier_process
from analysis import analysis_process
from pyqt_app import MainWindow
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication([])
    raw_bars_queue = multiprocessing.Queue()
    command_queue = multiprocessing.Queue()
    analysis_queue = multiprocessing.Queue()

    # Start the data receiver process
    receiver_process = multiprocessing.Process(
        target=analysis_process,
        args=(raw_bars_queue, analysis_queue, command_queue),
        daemon=True
    )
    receiver_process.start()

    # Start the data supplier process
    supplier_process = multiprocessing.Process(
        target=bars_supplier_process,
        args=(raw_bars_queue,),
        daemon=True
    )
    supplier_process.start()
        # Create the GUI window
    window = MainWindow(analysis_queue)
    window.show()

    # Start the application event loop
    app.exec()

    # try:
    #     # Keep the main process running until interrupted
    #     receiver_process.join()
    #     supplier_process.join()
    # except KeyboardInterrupt:
    #     print("Main process interrupted by keyboard.")

if __name__ == "__main__":
    main()
