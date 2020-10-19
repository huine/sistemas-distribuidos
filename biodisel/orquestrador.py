from Logger import Logger
from Reator import Reator
from datetime import datetime
from threading import Thread


def logger_start(logger):
    """."""
    logger.start_logger()


if __name__ == "__main__":
    logger = Logger()
    thread_logger = Thread(
        target=logger_start, args=(logger, ), name="Logger",
        daemon=True)
    reator = Reator()
    

    thread_logger.start()
    reator.start()
    

    start = datetime.now()
    print('start %s' % start)
    while (datetime.now() - start).total_seconds() < 10:
        pass

    reator.stop()
    logger.stop_logger()

    print('Fim')
