import logging


class Logger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_error(self, message, exception=None):
        self.logger.exception(message, exc_info=exception)

    def log_info(self, message):
        self.logger.info(message)


# export logger
logger = Logger("error.log")
