import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "console": {"()": "utils.log_formatter.ConsoleFormatter"},
            "main": {
                "format": '{"remote_address": "", '
                '"l": "", '
                '"username": "", '
                '"status_line": "", '
                '"status": "", '
                '"response_length": "", '
                '"refer": "", '
                '"user_agent": "", '
                '"host": "", '
                '"origin": "", '
                '"name": "", '
                '"level": "", '
                '"message": "", '
                '"log": {'
                '"name": "%(name)s", '
                '"message": "%(message)s", '
                '"title": "%(title)s", '
                '"additional_data": %(additional_data)s}}',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
        },
        "loggers": {
            # Root logger
            "": {
                "level": "INFO",
                "handlers": ["console"],
            },
            "custom": {
                "level": "INFO",
                "handlers": (["console"]),
                "propagate": False,
            },
        },
    }
)
