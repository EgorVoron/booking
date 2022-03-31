import datetime
import time


def unix2datetime(unix_time):
    return datetime.datetime.utcfromtimestamp(unix_time).strftime('%d.%m %H:%M')


def qt_time_to_unix(qt_time):
    return int(time.mktime((qt_time.dateTime().toPyDateTime() + datetime.timedelta(hours=3)).timetuple()))
