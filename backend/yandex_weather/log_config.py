import gzip
import os
import pathlib
import shutil
from datetime import time
from logging.handlers import TimedRotatingFileHandler


def get_logconfig(log_level: str) -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "formatter": {
                "format": "[{levelname} {asctime}] {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "formatter": "formatter",
                "class": "logging.StreamHandler",
            },
            "debug_to_file": {
                "level": "DEBUG",
                "formatter": "formatter",
                "class": "yandex_weather.log_config.CustomHandler",
                "filename": "../logs/debug/debug.log",
                "when": "H",
                "interval": 24,
            },
            "error_to_file": {
                "level": "ERROR",
                "formatter": "formatter",
                "class": "yandex_weather.log_config.CustomHandler",
                "filename": "../logs/error/error.log",
                "when": "H",
                "interval": 24,
            },
        },
        "loggers": {
            "django": {
                "level": log_level,
                "handlers": (
                    ["console", "debug_to_file"]
                    if log_level == "DEBUG"
                    else ["console", "error_to_file"]
                ),
            },
        },
    }


def rotator(source, dest):
    with open(source, "rb") as f_in:
        with gzip.open(dest, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(source)


def namer(name):
    return name + ".gz"


class CustomHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        filename: str,
        when: str = "h",
        interval: int = 1,
        backupCount: int = 30,
        encoding: str | None = None,
        delay: bool = False,
        utc: bool = False,
        atTime: time | None = None,
        errors: str | None = None,
    ) -> None:
        pathlib.Path("../logs/error/").mkdir(parents=True, exist_ok=True)
        pathlib.Path("../logs/debug/").mkdir(parents=True, exist_ok=True)
        self.rotator = rotator
        self.namer = namer
        super().__init__(
            filename,
            when,
            interval,
            backupCount,
            encoding,
            delay,
            utc,
            atTime,
            errors,
        )
