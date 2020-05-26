import asyncio
import time
import logging
from dataclasses import dataclass
from proxyscrape.proxyscrape_checker import ProxyScrapeChecker


@dataclass
class ProxyScrapeRunner:
    _proxyscrape_checker: ProxyScrapeChecker = ProxyScrapeChecker()

    def run_proxyscrape_job(self):
        logging.info(f'ProxyScrape Job starting...')
        start_time = time.time()
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._proxyscrape_checker.check_proxies())
        except Exception as ex:
            print(ex)

        logging.info(f'ProxyScrape Job took: {time.time() - start_time}')
