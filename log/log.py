import sys
import os
import re
import time
import threading
import logging
from logging.handlers import TimedRotatingFileHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from filesystem import filesystem


class Cutter:
    def __init__(self, director, level, format="%Y-%m-%d"):
        self.level = level
        self.format = format
        self.director = director
        self.file = None
        self.mutex = threading.RLock()

    def write(self, message):
        with self.mutex:
            if self.file:
                self.file.close()
                self.file = None

            business = ""
            if "business" in message:
                match = re.search(r'"business": "([^,]+)"', message)
                if match:
                    business = match.group(1)
                    message = re.sub(r'"business": "([^,]+)"', "", message)

            format_date = time.strftime(self.format)
            filename = os.path.join(
                self.director, format_date, business, f"{self.level}.log"
            )
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            self.file = open(filename, "a")
            self.file.write(message)
            self.file.flush()


class ZapProvider:
    def __init__(self, path: str, in_console: bool):
        self.path = path
        self.in_console = in_console
        self.logger = logging.getLogger("ZapProvider")
        self.logger.setLevel(logging.DEBUG)
        self._setup_loggers()

    def _setup_loggers(self):
        levels = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
        for level in levels:
            
            fs = filesystem.new_by_relative(self.path)
            if not fs.is_dir:
                fs.mkdir()
            
            handler = TimedRotatingFileHandler(
                os.path.join(self.path, f"{level.lower()}.log"),
                when="midnight",
                interval=1,
                backupCount=7,
            )
            handler.setLevel(getattr(logging, level))
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            if self.in_console:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(getattr(logging, level))
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

    def log(self, level, message:str):
        getattr(self.logger, level.lower())(message)


if __name__ == "__main__":
    # Example usage
    zap_provider = ZapProvider("logs", True)
    zap_provider.log("info", '{"business": "example"} This is an info message')
