import asyncio
import time
import logging
from dataclasses import dataclass
from pldown.pldown_checker import PldownChecker


@dataclass
class PldownRunner:
    _pldown_checker: PldownChecker = PldownChecker()

    def run_pldown_job(self):
        logging.info(f'Pldown Job starting...')
        start_time = time.time()
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._pldown_checker.check_proxies())
        except Exception:
            pass

        logging.info(f'Pldown Job took: {time.time() - start_time}')
