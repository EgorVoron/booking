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

        building_label = QtWidgets.QLabel(self)
        building_label.setText("Корпус:")
        building_label.adjustSize()
        building_label.move(30, 107)

        combo = QtWidgets.QComboBox(self)
        combo.addItem("Любой")
        combo.addItem("Главный (гк)")
        combo.addItem("Лабораторный (лк)")
        combo.addItem("Новый (нк)")
        combo.move(100, 100)

        number_label = QtWidgets.QLabel(self)
        number_label.setText("Кол-во людей:")
        number_label.adjustSize()
        number_label.move(250, 107)

        line = QtWidgets.QLineEdit(self)
        line.move(350, 100)
        onlyInt = QIntValidator()
        line.setValidator(onlyInt)

        start_datetime = QDateTimeEdit(self)
        start_datetime.setGeometry(580, 100, 150, 30)
        cur_dt = QDateTime.currentDateTime()
        start_datetime.setDateTime(cur_dt)
        start_label = QLabel("Время начала:", self)
        start_label.setGeometry(480, 85, 200, 60)
        start_label.setWordWrap(True)
        start_warning = QLabel("", self)
        start_warning.setGeometry(580, 140, 200, 60)
        start_warning.setWordWrap(True)
        start_datetime.dateTimeChanged.connect(lambda: dt_method(start_datetime))

        def dt_method(start_datetime, win=self):
            if start_datetime.dateTime().toPyDateTime() < datetime.datetime.now():
                start_warning.setText('Время начала не может быть раньше текущего!')
                win.time_problem = True
            else:
                win.time_problem = False
                start_warning.setText('')

        end_datetime = QDateTimeEdit(self)
        end_datetime.setDateTime(cur_dt)
        end_datetime.setGeometry(880, 100, 150, 30)
        end_label = QLabel("Время конца:", self)
        end_label.setGeometry(780, 85, 200, 60)
        end_label.setWordWrap(True)
        end_warning = QLabel("", self)
        end_warning.setGeometry(880, 140, 200, 60)
        end_warning.setWordWrap(True)
        end_datetime.dateTimeChanged.connect(lambda: dt_method2(end_datetime))

        def dt_method2(end_datetime, win=self):
            if end_datetime.dateTime().toPyDateTime() < start_datetime.dateTime().toPyDateTime():
                end_warning.setText('Время конца не может быть меньше времени начала!')
                win.time_problem = True
            elif end_datetime.dateTime().toPyDateTime() - start_datetime.dateTime().toPyDateTime() > datetime.timedelta(
                    hours=5):
                end_warning.setText('Нельзя бронировать больше, чем на 5 часов!')
                win.time_problem = True
            elif end_datetime.dateTime().toPyDateTime() == start_datetime.dateTime().toPyDateTime():
                end_warning.setText('Время начала и конца не может совпадать!')
                win.same_time = True
            else:
                win.same_time = False
                win.time_problem = False
                end_warning.setText('')
            print(end_datetime.dateTime().toPyDateTime())
            print(start_datetime.dateTime().toPyDateTime())

        error_label = QLabel("", self)
        error_label.setGeometry(100, 200, 200, 15)

        def run(win=self):
            if not line.text():
                error_label.setText('Введите число людей!')
                print('Введите число людей!')
            elif win.time_problem:
                error_label.setText('Исправьте время')
                print('Исправьте время')
            elif win.same_time:
                error_label.setText('Время начала и конца совпадает!')
                print('Иремя начала и конц')
            else:
                print('h')
                error_label.setText('')
                get_recommendations(start_time=qt_time_to_unix(start_datetime),
                                    end_time=qt_time_to_unix(end_datetime),
                                    people_num=int(line.text()),
                                    building=str(combo.currentText()))
                self.show_results()
            res_lab = QLabel("ПИЗДА", win)
            res_lab.setGeometry(100, 200, 200, 15)

        button = QtWidgets.QPushButton(self)
        button.clicked.connect(lambda: run())
        button.setText("Найти подходящие комнаты")
        button.setGeometry(100, 250, 200, 50)

    def show_results(self):
        button = QtWidgets.QPushButton(self)
        button.setText("Найти adsasda комнаты")
        button.setGeometry(100, 300, 200, 50)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
