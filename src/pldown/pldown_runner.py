import time
import logging
from pldown.pldown_checker import PldownChecker


class PldownRunner:

    def __init__(self):
        self.__checker = PldownChecker()

    def run_pldown_job(self, loop):
        logging.info(f'Pldown Job starting...')
        start_time = time.time()

        try:
            loop.run_until_complete(self.__checker.check_proxies())
        except Exception as ex:
            logging.error(ex)
            pass

        logging.info(f'Pldown Job took: {time.time() - start_time}')
