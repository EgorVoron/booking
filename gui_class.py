from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QDateTimeEdit
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import sys
from main import get_recommendations
import datetime

import sys

WIN_WIDTH = 1200
WIN_HEIGHT = 700


def qt_time_to_unix(qt_time):
    return int(time.mktime(qt_time.dateTime().toPyDateTime().timetuple()))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Бронь аудиторий")
        center = QDesktopWidget().availableGeometry().center()
        self.setGeometry(center.x() - WIN_WIDTH // 2, center.y() - WIN_HEIGHT // 2, WIN_WIDTH, WIN_HEIGHT)
        self.UiComponents()
        self.show()

    # method for components
    def UiComponents(self):
        self.time_problem = False
        self.same_time = True

        self.building_label = QtWidgets.QLabel(self)
        self.building_label.setText("Корпус:")
        self.building_label.adjustSize()
        self.building_label.move(30, 107)

        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItem("Любой")
        self.combo.addItem("Главный (гк)")
        self.combo.addItem("Лабораторный (лк)")
        self.combo.addItem("Новый (нк)")
        self.combo.move(100, 100)

        self.number_label = QtWidgets.QLabel(self)
        self.number_label.setText("Кол-во людей:")
        self.number_label.adjustSize()
        self.number_label.move(250, 107)

        self.line = QtWidgets.QLineEdit(self)
        self.line.move(350, 100)
        self.onlyInt = QIntValidator()
        self.line.setValidator(self.onlyInt)

        self.start_datetime = QDateTimeEdit(self)
        self.start_datetime.setGeometry(580, 100, 150, 30)
        self.cur_dt = QDateTime.currentDateTime()
        self.start_datetime.setDateTime(self.cur_dt)
        self.start_label = QLabel("Время начала:", self)
        self.start_label.setGeometry(480, 85, 200, 60)
        self.start_label.setWordWrap(True)
        self.start_warning = QLabel("", self)
        self.start_warning.setGeometry(580, 140, 200, 60)
        self.start_warning.setWordWrap(True)
        self.start_datetime.dateTimeChanged.connect(lambda: self.dt_method(self.start_datetime))

        self.end_datetime = QDateTimeEdit(self)
        self.end_datetime.setDateTime(self.cur_dt)
        self.end_datetime.setGeometry(880, 100, 150, 30)
        self.end_label = QLabel("Время конца:", self)
        self.end_label.setGeometry(780, 85, 200, 60)
        self.end_label.setWordWrap(True)
        self.end_warning = QLabel("", self)
        self.end_warning.setGeometry(880, 140, 200, 60)
        self.end_warning.setWordWrap(True)
        self.end_datetime.dateTimeChanged.connect(lambda: self.dt_method2(self.end_datetime))

        button = QtWidgets.QPushButton(self)
        button.clicked.connect(self.run)
        button.setText("Найти подходящие комнаты")
        button.setGeometry(100, 250, 200, 50)

        error_label = QLabel("", self)
        error_label.setGeometry(100, 200, 200, 15)

    def dt_method(self, start_datetime):
        if start_datetime.dateTime().toPyDateTime() < datetime.datetime.now():
            self.start_warning.setText('Время начала не может быть раньше текущего!')
            self.time_problem = True
        else:
            self.time_problem = False
            self.start_warning.setText('')

    def dt_method2(self, end_datetime):
        if end_datetime.dateTime().toPyDateTime() < self.start_datetime.dateTime().toPyDateTime():
            self.end_warning.setText('Время конца не может быть меньше времени начала!')
            self.time_problem = True
        elif end_datetime.dateTime().toPyDateTime() - self.start_datetime.dateTime().toPyDateTime() > datetime.timedelta(
                hours=5):
            self.end_warning.setText('Нельзя бронировать больше, чем на 5 часов!')
            self.time_problem = True
        elif end_datetime.dateTime().toPyDateTime() == self.start_datetime.dateTime().toPyDateTime():
            self.end_warning.setText('Время начала и конца не может совпадать!')
            self.same_time = True
        else:
            self.same_time = False
            self.time_problem = False
            self.end_warning.setText('')

    def run(self):
        print(self.line.text())
        if not self.line.text():
            self.error_label.setText('Введите число людей!')
            print('Введите число людей!')
        elif self.time_problem:
            self.error_label.setText('Исправьте время')
            print('Исправьте время')
        elif self.same_time:
            self.error_label.setText('Время начала и конца совпадает!')
            print('Иремя начала и конц')
        else:
            self.error_label.setText('')
            get_recommendations(start_time=qt_time_to_unix(self.start_datetime),
                                end_time=qt_time_to_unix(self.end_datetime),
                                people_num=int(self.line.text()),
                                building=str(self.combo.currentText()))


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
