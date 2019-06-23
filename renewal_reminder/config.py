from dataclasses import dataclass
from os import environ


@dataclass
class AppConfig:
    file_path: str
    log_level: str
    token_id: str
    chat_id: str
    notice_days: int


def get_config() -> AppConfig:
    config = AppConfig(file_path=environ['APP_FILE_PATH'],
                       log_level=environ['APP_LOG_LEVEL'],
                       token_id=environ['APP_TOKEN_ID'],
                       chat_id=environ['APP_CHAT_ID'],
                       notice_days=int(environ['APP_NOTICE_DAYS']))
    return config
