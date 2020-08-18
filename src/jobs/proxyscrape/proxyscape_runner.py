import time
import logging


class ProxyScrapeRunner:

    def __init__(self, proxyscrape_checker):
        self._proxyscrape_checker = proxyscrape_checker

    def run_proxyscrape_job(self, loop):
        logging.info(f'ProxyScrape Job starting...')
        start_time = time.time()

        try:
            loop.run_until_complete(self._proxyscrape_checker.check_proxies())
        except Exception as ex:
            print(ex)

        logging.info(f'ProxyScrape Job took: {time.time() - start_time}')
