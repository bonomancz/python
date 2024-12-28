import datetime


class Time:

    def __init__(self):
        pass

    def get_milliseconds_datetime(self) -> str:
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
