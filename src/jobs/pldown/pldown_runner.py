import time
import logging


class PldownRunner:

    def __init__(self, pldown_checker):
        self._pldown_checker = pldown_checker

    def run_pldown_job(self, loop):
        logging.info(f'Pldown Job starting...')
        start_time = time.time()

        try:
            loop.run_until_complete(self._pldown_checker.check_proxies())
        except Exception as ex:
            logging.error(ex)
            pass

        logging.info(f'Pldown Job took: {time.time() - start_time}')
