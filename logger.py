import logging


class Logger:
    def __init__(self, error_log_file="error.log", warn_log_file="warn.log"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # error log store with file
        file_handler = logging.FileHandler(error_log_file)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        # info log output in console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        # warn log store with file
        warn_file_handler = logging.FileHandler(warn_log_file)
        warn_file_handler.setLevel(logging.WARN)
        warn_file_handler.setFormatter(formatter)
        self.logger.addHandler(warn_file_handler)

    def log_error(self, message, exception=None):
        self.logger.exception(message, exc_info=exception)

    def log_info(self, message):
        self.logger.info(message)

    def log_warn(self, message):
        self.logger.warn(message)


# export logger
logger = Logger()
