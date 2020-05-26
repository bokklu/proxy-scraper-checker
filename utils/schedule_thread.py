import threading
from scheduler import Scheduler


class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        scheduler = Scheduler()
        scheduler.schedule_jobs()
