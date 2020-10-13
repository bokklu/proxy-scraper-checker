import threading
import asyncio
import sys
import logging
from containers import Scheduler


class ScheduleThreadSecond(threading.Thread):
    @classmethod
    def run(cls):

        loop = None

        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
        elif sys.platform == 'linux':
            import uvloop
            loop = uvloop.new_event_loop()
        else:
            logging.error('Unsupported platform...')

        logging.info(f'Running on platform: {sys.platform}')
        asyncio.set_event_loop(loop)

        scheduler = Scheduler.scheduler_second()
        scheduler.schedule_jobs(loop)
