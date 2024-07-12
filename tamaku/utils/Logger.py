import logging
import sys


class Logger:
    def __init__(
            self,
            log_level='INFO',
            log_format='%(asctime)s - %(levelname)s - %(message)s',
            date_format='%Y-%m-%d %H:%M:%S'
    ):
        self.logger = self.setup_logging(log_level, log_format, date_format)

    @staticmethod
    def setup_logging(log_level, log_format, date_format):
        log_level = log_level.upper()

        stdout_handler = logging.StreamHandler(sys.stdout)
        stderr_handler = logging.StreamHandler(sys.stderr)

        stdout_handler.setLevel(log_level)
        stderr_handler.setLevel(log_level)

        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        stdout_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)

        logger = logging.getLogger('Logger')
        logger.setLevel(log_level)

        logger.handlers.clear()

        stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
        stderr_handler.addFilter(lambda record: record.levelno > logging.INFO)

        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)

        return logger

    def set_level(self, level):
        self.logger.setLevel(level.upper())

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
