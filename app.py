import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

from main_app import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    Window = MainWindow()
    Window.show()

    sys.exit(app.exec())