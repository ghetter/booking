import logging
from loguru import logger


class DjangoLoguruHandler(logging.Handler):
    def __init__(self)-> None:
        logger.remove()
        logging.Handler.__init__(self=self)
        logger.add(
            'logs/django.log',
            level='DEBUG',
            rotation='10 MB',
            backtrace=True,
        )

    def emit(self, record: logging.LogRecord) -> None:
        level = record.levelname
        message = record.message
        logger.log(level, message)

