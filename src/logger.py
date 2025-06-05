# Простейший класс логирования
import logging

logger = logging.getLogger("vehicle_detector")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

class Logger:
    """Сбор и вывод сообщений в консоль."""

    def __init__(self):
        self.logs = []

    def log(self, message, level="INFO"):
        log_entry = f"{level} - {message}"
        self.logs.append(log_entry)
        if level == "INFO":
            logger.info(message)
        elif level == "ERROR":
            logger.error(message)
        elif level == "DEBUG":
            logger.debug(message)
        elif level == "WARNING":
            logger.warning(message)

    def get_logs(self):
        return self.logs

    def clear_logs(self):
        self.logs = []
