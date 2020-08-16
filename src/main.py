import logging
from logging.handlers import TimedRotatingFileHandler
from src.utils.schedule_thread import ScheduleThread

if __name__ == "__main__":
    logging.raiseExceptions = False
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
                        handlers=[TimedRotatingFileHandler("log-file.log", when="D", interval=7, backupCount=0), logging.StreamHandler()])

    schedule_thread = ScheduleThread()
    schedule_thread.start()
