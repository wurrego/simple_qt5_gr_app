import signal
import sys
from PyQt5 import QtWidgets

from cog_tx.version import __version__
from cog_tx.ui_classes.cog_tx_main_window import CogTransmit_MainWindow

def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setOrganizationName("VT")
        app.setOrganizationDomain("www.vt.edu")
        app.setApplicationName("Cogswill Tx App")
        app.setApplicationVersion(__version__)

        CogTransmit_MainWindow.window = CogTransmit_MainWindow()

        sys.exit(app.exec_())

    finally:
        print('Done')

if __name__ == "__main__":
    main()