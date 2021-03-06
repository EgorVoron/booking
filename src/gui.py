from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QDateTimeEdit
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import datetime

from core import get_recommendations, post_booking, get_bookings
from utils import qt_time_to_unix
from objects import Interval

WIN_WIDTH = 1200
WIN_HEIGHT = 900


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Бронь аудиторий")
        center = QDesktopWidget().availableGeometry().center()
        self.setGeometry(center.x() - WIN_WIDTH // 2, center.y() - WIN_HEIGHT // 2, WIN_WIDTH, WIN_HEIGHT)
        self.UiComponents()
        self.show()
        self.time_problem = False
        self.same_time = True

    def UiComponents(self):
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
        only_int = QIntValidator()
        line.setValidator(only_int)

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

        error_label = QLabel("", self)
        error_label.setGeometry(100, 200, 200, 15)

        button = QtWidgets.QPushButton(self)
        button.clicked.connect(lambda: run())
        button.setText("Найти подходящие комнаты")
        button.setGeometry(100, 250, 200, 50)

        to_book = QLabel("Выберите комнату для бронирования:", self)
        to_book.setGeometry(100, 300, 500, 30)
        to_book.setWordWrap(True)
        to_book.setHidden(True)

        combo2 = QtWidgets.QComboBox(self)
        combo2.move(380, 300)
        combo2.setHidden(True)

        book_button = QtWidgets.QPushButton(self)
        book_button.clicked.connect(lambda: book())
        book_button.setText("Забронировать!")
        book_button.setGeometry(100, 350, 200, 50)
        book_button.setHidden(True)

        bookings_label = QtWidgets.QLabel(f'Ваши брони: \n{get_bookings()}', self)
        bookings_label.setGeometry(100, 450, 300, 200)
        bookings_label.setHidden(False)

        def run(win=self):
            if not line.text():
                error_label.setText('Введите число людей!')
                print('Введите число людей!')
            elif win.time_problem:
                error_label.setText('Исправьте время')
                print('Исправьте время')
            elif win.same_time:
                error_label.setText('Время начала и конца совпадает!')
                print('Время начала и конца совпадает!')
            else:
                error_label.setText('')
                self.start_time = qt_time_to_unix(start_datetime)
                self.end_time = qt_time_to_unix(end_datetime)
                valid_rooms = get_recommendations(start_time=self.start_time,
                                                  end_time=self.end_time,
                                                  people_num=int(line.text()),
                                                  building=str(combo.currentText()))
                if not valid_rooms:
                    to_book.setHidden(True)
                    combo2.setHidden(True)
                    book_button.setHidden(True)
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Свободных аудиторий в указанный интервал не найдено. Попробуйте другой интервал")
                    msg.setWindowTitle("Не найдено")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
                self.valid_rooms = valid_rooms
                valid_rooms_text = '\n'.join([f'{room.room_number}, {room.building}' for room in valid_rooms[:10]])
                self.valid_rooms_text = valid_rooms_text
                to_book.setHidden(False)
                combo2.clear()
                combo2.addItems([f'{room.room_number}, {room.building}' for room in valid_rooms[:10]])
                combo2.setHidden(False)
                book_button.setHidden(False)

        def book():
            room = self.valid_rooms[self.valid_rooms_text.index(combo2.currentText())]
            interval = Interval(self.start_time,
                                self.end_time)
            post_booking(room,
                         interval)
            bookings_label.setText(bookings_label.text() + f'\n{combo2.currentText()}: {str(interval)}')
            to_book.setHidden(True)
            combo2.setHidden(True)
            book_button.setHidden(True)

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Успешно забронировано!")
            msg.setWindowTitle("Готово")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
