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

    def schedule_jobs(self, loop):
        logging.info('Starting scheduler...')

        schedule.every(1).hour.at(':00').do(self._pldown_runner.run_pldown_job, loop)
        schedule.every(2).hours.at(':00').do(self._proxyscrape_runner.run_proxyscrape_job, loop)

        while True:
            schedule.run_pending()
            time.sleep(1)
