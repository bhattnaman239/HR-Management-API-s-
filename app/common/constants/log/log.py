import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "app.log",  
        },
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["file", "console"],
            "propagate": False
        },
        "fastapi": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("fastapi")
