import schedule
import time
import logging
from pldown.pldown_runner import PldownRunner
from proxyscrape.proxyscape_runner import ProxyScrapeRunner
from dataclasses import dataclass


@dataclass
class Scheduler:
    _pldown_runner: PldownRunner = PldownRunner()
    _proxyscrape_runner: ProxyScrapeRunner = ProxyScrapeRunner()

    def schedule_jobs(self):
        logging.info('Starting scheduler...')

        schedule.every(1).hour.do(self._pldown_runner.run_pldown_job)
        schedule.every(5).hours.do(self._proxyscrape_runner.run_proxyscrape_job)
        self._pldown_runner.run_pldown_job()

        while True:
            schedule.run_pending()
            time.sleep(1)
