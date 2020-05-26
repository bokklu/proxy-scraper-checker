import threading
import asyncio
import sys
import logging
from scheduler import Scheduler


class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):

        loop = None

        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
        elif sys.platform == 'linux':
            loop = asyncio.SelectorEventLoop()
        else:
            logging.error('Unsupported platform...')

        asyncio.set_event_loop(loop)

        scheduler = Scheduler()
        scheduler.schedule_jobs(loop)
