from sympy.plotting.intervalmath import interval

from objects import Interval, Room
from sql_parsing import db


# people_num = 10
# building = ''
# start_time = 100
# end_time = 200


def get_recommendations(start_time, end_time, people_num, building):
    building = None if building == 'Любой' else building
    rooms = db.get_recommended_rooms(start_time,
                                     end_time,
                                     people_num=people_num,
                                     building=building)

    return rooms


def post_booking(room: Room, interval: Interval):
    db.book(room, interval)

# try:
#     interval = Interval(start_time, end_time)
# except ValueError as ex:
#     print(ex)

# rooms = db.get_recommended_rooms(interval.start_time,
#                            interval.end_time,
#                            people_num=people_num,
#                            building=building)
#
# for room in rooms:
#     print(room)
#
# all_rooms = db.get_all_rooms()
# print(all_rooms)
