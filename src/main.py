import sys
from PyQt5.QtWidgets import *
from gui import Window

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
