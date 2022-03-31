from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
import sys

app = QApplication(sys.argv)
win = QMainWindow()

WIN_WIDTH = 1000
WIN_HEIGHT = 700

center = QDesktopWidget().availableGeometry().center()
win.setGeometry(center.x() - WIN_WIDTH // 2, center.y() - WIN_HEIGHT // 2, WIN_WIDTH, WIN_HEIGHT)
win.setWindowTitle("NME")

combo = QtWidgets.QComboBox(win)
combo.addItem("Python")
combo.addItem("Java")
combo.addItem("C++")
combo.move(100, 100)

button = QtWidgets.QPushButton(win)
button.setText("A Button")
button.move(300, 100)

win.show()
sys.exit(app.exec_())
