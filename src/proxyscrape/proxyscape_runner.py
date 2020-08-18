import time
import logging
from proxyscrape.proxyscrape_checker import ProxyScrapeChecker


class ProxyScrapeRunner:

    def __init__(self):
        self.__checker = ProxyScrapeChecker()

    def run_proxyscrape_job(self, loop):
        logging.info(f'ProxyScrape Job starting...')
        start_time = time.time()

        try:
            loop.run_until_complete(self.__checker.check_proxies())
        except Exception as ex:
            print(ex)

        logging.info(f'ProxyScrape Job took: {time.time() - start_time}')
