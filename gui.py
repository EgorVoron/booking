from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QDateTimeEdit
from PyQt5.QtCore import QDateTime, QTime
import sys

app = QApplication(sys.argv)
win = QMainWindow()

WIN_WIDTH = 1000
WIN_HEIGHT = 700

center = QDesktopWidget().availableGeometry().center()
win.setGeometry(center.x() - WIN_WIDTH // 2, center.y() - WIN_HEIGHT // 2, WIN_WIDTH, WIN_HEIGHT)
win.setWindowTitle("NME")

label = QtWidgets.QLabel(win)
label.setText("Корпус:")
label.adjustSize()
label.move(30, 100)

combo = QtWidgets.QComboBox(win)
combo.addItem("Любой")
combo.addItem("Главный (гк)")
combo.addItem("Лабораторный (лк)")
combo.addItem("Новый (нк)")
combo.move(100, 100)

label = QtWidgets.QLabel(win)
label.setText("Кол-во людей:")
label.adjustSize()
label.move(250, 100)

line = QtWidgets.QLineEdit(win)
line.move(350, 100)
# print(str(combo.currentText()))


datetimeedit = QDateTimeEdit()
datetimeedit.move(400, 100)
datetimeedit.setDateTime(QDateTime(2020, 10, 10, 11, 30))
time = QTime(21, 45)
datetimeedit.setTime(time)


# button = QtWidgets.QPushButton(win)
# button.setText("A Button")
# button.move(300, 100)

win.show()
sys.exit(app.exec_())
