import logging
import os
from logging.handlers import TimedRotatingFileHandler
from utils.schedule_thread import ScheduleThread
from utils.schedule_thread_second import ScheduleThreadSecond
from config import DevelopmentConfig, ProductionConfig
from containers import Configs


if __name__ == "__main__":
    logging.raiseExceptions = False
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
                        handlers=[TimedRotatingFileHandler("log-file.log", when="D", interval=7, backupCount=0), logging.StreamHandler()])

    try:
        env = os.environ["PSC_ENVIRONMENT"]

        if env == 'Development':
            config = DevelopmentConfig()
        else:
            db_pass = os.environ["PSC_DBPASSWORD"]
            config = ProductionConfig()
            config.sql['password'] = db_pass

    except KeyError as key_error:
        logging.fatal('Environment variable not set!')
        raise key_error

    Configs.config.override(config.asdict())

    schedule_thread = ScheduleThread()
    schedule_thread_second = ScheduleThreadSecond()
    schedule_thread.start()
    schedule_thread_second.start()
    schedule_thread.join()
    schedule_thread_second.join()
