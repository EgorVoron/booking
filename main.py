from objects import Interval, Room
from sql_parsing import db

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
