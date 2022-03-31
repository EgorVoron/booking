import sqlite3
from objects import Interval, Room


class sql_parser:
    def __init__(self):
        self.db_name = '1c.db'

    def get_recommended_rooms(self, start_time, end_time, people_num, building=None):
        sqlite_conn = sqlite3.connect(self.db_name)
        cursor = sqlite_conn.cursor()
        cursor.execute(
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
        sqlite_conn.commit()
        rooms = [Room(*room_list) for room_list in cursor.fetchall()]
        sqlite_conn.close()
        return rooms

    def book(self, room: Room, interval: Interval):
        sqlite_conn = sqlite3.connect(self.db_name)
        cursor = sqlite_conn.cursor()
        valid_rooms = self.get_recommended_rooms(interval.start_time, interval.end_time, room.capacity, room.building)
        if room.room_id not in [valid_room.room_id for valid_room in valid_rooms]:
            print('already exists')
            return
        q1 = f"""insert into interval values ({interval.interval_id}, {interval.start_time}, {interval.end_time})"""
        cursor.execute(q1)
        sqlite_conn.commit()

        q2 = f"""insert into room_interval values ({room.room_id}, {interval.interval_id})"""
        cursor.execute(q2)
        sqlite_conn.commit()
        sqlite_conn.close()

    def get_booked_intervals(self):
        sqlite_conn = sqlite3.connect(self.db_name)
        cursor = sqlite_conn.cursor()
        q1 = f"""select distinct room_number, building, start_time, end_time
from (room
left outer join room_interval on room.room_id = room_interval.room_id
left outer join interval on room_interval.interval_id = interval.interval_id)
where not (start_time is null)"""
        cursor.execute(q1)
        bookings = list(cursor.fetchall())
        print('bookings', bookings)
        sqlite_conn.commit()
        sqlite_conn.close()
        return bookings


db = sql_parser()

# if __name__ == '__main__':
#     # db.book(Room(11, 1, 10, 'lab'), Interval(1648734639, 1648734939))
#     print(db.book(Room(11, 1, 10, 'lab'), Interval(1648740994, 1648741054)))
