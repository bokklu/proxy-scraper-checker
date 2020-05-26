import time
import logging
from dataclasses import dataclass
from proxyscrape.proxyscrape_checker import ProxyScrapeChecker


@dataclass
class ProxyScrapeRunner:
    _proxyscrape_checker: ProxyScrapeChecker = ProxyScrapeChecker()

    def run_proxyscrape_job(self, loop):
        logging.info(f'ProxyScrape Job starting...')
        start_time = time.time()

        try:
            loop.run_until_complete(self._proxyscrape_checker.check_proxies())
        except Exception as ex:
            print(ex)

        logging.info(f'ProxyScrape Job took: {time.time() - start_time}')
