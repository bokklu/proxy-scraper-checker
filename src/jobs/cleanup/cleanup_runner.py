import logging
import time


class CleanupRunner:

    def __init__(self, cleanup_checker):
        self.__checker = cleanup_checker

    def run_cleanup_job(self, loop):
        logging.info(f'Cleanup Job starting...')
        start_time = time.time()

        try:
            loop.run_until_complete(self.__checker.cleanup_proxies())
        except Exception as ex:
            logging.error(ex)
            pass

        logging.info(f'Cleanup Job took: {time.time() - start_time}')
