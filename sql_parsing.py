import sqlite3
from objects import Interval, Room


class sql_parser:
    def __init__(self):
        db_name = '2c.db'
        self.sqlite_conn = sqlite3.connect(db_name)
        self.cursor = self.sqlite_conn.cursor()

    def get_recommended_rooms(self, start_time, end_time, people_num, building=None):
        self.cursor.execute(
            f"""select room_id, room_number, capacity, building 
        from room 
        where (capacity >= {people_num} and room_id not in (
            select room_id from room_interval where interval_id in (
                select interval_id
                from interval
                where (start_time <= {start_time} and end_time >= {start_time})
                    or (start_time <= {end_time} and end_time >= {end_time})
                    or (start_time >= {start_time} and end_time <= {end_time})
            )) {f"and building = '{building}'" if building else ''}
        )
            """
        )
        return [Room(*room_list) for room_list in self.cursor.fetchall()]

    def book(self, room: Room, interval: Interval):
        print('a')
        q1 = f"""insert into interval values ({interval.interval_id}, {interval.start_time}, {interval.end_time})"""
        print(q1)
        self.cursor.execute(q1)
        q2 = f"""insert into room_interval values ({room.room_id}, {interval.interval_id})"""
        self.cursor.execute(q2)
        self.sqlite_conn.commit()
        self.cursor.close()
        print('b')


def get_all_rooms(self):
    self.cursor.execute("""select * from room""")
    return [Room(*room_list) for room_list in self.cursor.fetchall()]


db = sql_parser()
