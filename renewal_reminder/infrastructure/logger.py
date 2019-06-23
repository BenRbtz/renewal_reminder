from json import dumps as json_dumps
from logging import Formatter, LogRecord, getLogger
from logging.config import dictConfig
from typing import Optional

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'json': {
            'class': 'renewal_reminder.infrastructure.logger.JsonFormatter'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'stream': 'ext://sys.stderr',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}


class JsonFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        format_data = {
            'timestamp': self.formatTime(record=record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
        }
        return json_dumps(format_data)


def get_logger(log_level: str, log_config: Optional[dict] = None):
    log_config = log_config or LOG_CONFIG
    dictConfig(log_config)
    logger = getLogger()
    logger.setLevel(log_level)

    return logger
