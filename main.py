import logging
from utils.schedule_thread import ScheduleThread

if __name__ == "__main__":
    logging.raiseExceptions = False
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("log-file.log"), logging.StreamHandler()])

    schedule_thread = ScheduleThread()
    schedule_thread.start()
