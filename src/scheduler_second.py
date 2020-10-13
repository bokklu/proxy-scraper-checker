import schedule
import time
import logging


class SchedulerSecond:

    def __init__(self, pldown_runner, proxyscrape_runner, cleanup_runner):
        self._pldown_runner = pldown_runner
        self._proxyscrape_runner = proxyscrape_runner
        self._cleanup_runner = cleanup_runner

    def schedule_jobs(self, loop):
        logging.info('Starting scheduler...')

        schedule.every(2).hours.at(':00').do(self._proxyscrape_runner.run_proxyscrape_job, loop).run()

        while True:
            schedule.run_pending()
            time.sleep(1)
