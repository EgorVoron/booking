from dataclasses import dataclass
from random import randint

MAX_INTERVAL_LEN = 1000


class Interval:
    def __init__(self, start_time, end_time):
        self.interval_id = randint(1, int(1e8))
        self.start_time = start_time
        self.end_time = end_time


@dataclass
class Room:
    room_id: int
    room_number: int
    capacity: int
    building: str
