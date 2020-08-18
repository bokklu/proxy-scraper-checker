import schedule
import time
import logging
from pldown.pldown_runner import PldownRunner
from proxyscrape.proxyscape_runner import ProxyScrapeRunner


class Scheduler:

    def __init__(self):
        self.__pldown_runner = PldownRunner()
        self.__proxyscrape_runner = ProxyScrapeRunner()

    def schedule_jobs(self, loop):
        logging.info('Starting scheduler...')

        schedule.every(1).hour.at(':00').do(self.__pldown_runner.run_pldown_job, loop).run()
        schedule.every(2).hours.at(':00').do(self.__proxyscrape_runner.run_proxyscrape_job, loop).run()

        while True:
            schedule.run_pending()
            time.sleep(1)
