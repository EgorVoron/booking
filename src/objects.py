from dataclasses import dataclass
from random import randint

from src.utils import unix2datetime

MAX_INTERVAL_LEN = 1000


class Interval:
    def __init__(self, start_time, end_time):
        self.interval_id = randint(1, int(1e8))
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f'{unix2datetime(self.start_time)} -- {unix2datetime(self.end_time)}'


@dataclass
class Room:
    room_id: int
    room_number: int
    capacity: int
    building: str
