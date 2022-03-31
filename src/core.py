from objects import Interval, Room
from db_parser import db
import time

building2code = {'Любой': None,
                 'Лабораторный (лк)': 'ЛК',
                 'Новый (нк)': 'НК',
                 'Главный (гк)': 'ГК'
                 }


def get_recommendations(start_time, end_time, people_num, building):
    rooms = db.get_recommended_rooms(start_time,
                                     end_time,
                                     people_num=people_num,
                                     building=building2code[building])
    return rooms


def post_booking(room: Room, interval: Interval):
    db.book(room, interval)


def get_bookings():
    bookings = sorted(db.get_booked_intervals(int(time.time())), key=lambda x: f'{x[2]}{x[3]}')
    return '\n'.join([f'{b[0]}, {b[1]}: {Interval(b[2], b[3])}' for b in bookings])
