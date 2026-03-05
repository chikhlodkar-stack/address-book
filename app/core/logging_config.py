from logging.config import dictConfig


def configure_logging():
    """
    Configures application-wide logging.
    """
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(levelname)s:     %(asctime)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "format": "%(levelname)s:     %(asctime)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "default",
                "class": "logging.StreamHandler",  # Logs to console
                "stream": "ext://sys.stdout",
            },
            "access": {
                "level": "INFO",
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "app": {  # Custom logger for our application code
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {  # Uvicorn's root logger
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {  # Uvicorn's error logger
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {  # Uvicorn's access logger (for HTTP requests)
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
            "sqlalchemy": {  # SQLAlchemy logger
                "handlers": ["default"],
                "level": "WARNING",  # Keep this at WARNING or higher in production
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["default"],
            "level": "WARNING",
        },
    }
    dictConfig(LOGGING_CONFIG)
