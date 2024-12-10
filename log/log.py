import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, dir):
        self.dir = os.path.join(dir, datetime.now().strftime('%Y-%m-%d'))
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def _generate_logger(self, level):
        logger = logging.getLogger(level)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(os.path.join(self.dir, f'{level}.log'))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def info(self, content):
        logger = self._generate_logger('info')
        logger.info(content)

    def warn(self, content):
        logger = self._generate_logger('warn')
        logger.warning(content)

    def error(self, content):
        logger = self._generate_logger('error')
        logger.error(content)

# 使用示例
logger = Logger("./logs")
logger.info({"msg":"info message"})
logger.warn("warn message")
logger.error("error message")