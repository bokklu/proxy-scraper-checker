import schedule
import time
import logging


class Scheduler:

    def __init__(self, pldown_runner, proxyscrape_runner, cleanup_runner):
        self._pldown_runner = pldown_runner
        self._proxyscrape_runner = proxyscrape_runner
        self._cleanup_runner = cleanup_runner

    def schedule_jobs(self, loop):
        logging.info('Starting scheduler...')

        schedule.every(1).hour.at(':00').do(self._pldown_runner.run_pldown_job, loop).run()

        while True:
            schedule.run_pending()
            time.sleep(1)
