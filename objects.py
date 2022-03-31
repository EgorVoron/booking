from dataclasses import dataclass
from random import randint

MAX_INTERVAL_LEN = 1000


class Interval:
    def __init__(self, start_time, end_time):
        if end_time < start_time:
            raise ValueError('Время завершения не может быть меньше времени старта!')
        if end_time - start_time > MAX_INTERVAL_LEN:
            raise ValueError('Бронить больше чем на 5ч нельзя!')
        self.interval_id = randint(1, int(1e8))
        self.start_time = start_time
        self.end_time = end_time


@dataclass
class Room:
    room_id: int
    room_number: int
    capacity: int
    building: str
