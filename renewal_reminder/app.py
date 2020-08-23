import logging
from dataclasses import dataclass
from os import environ
from typing import Optional

from renewal_reminder.business_logic.checker import RenewalChecker
from renewal_reminder.infrastructure.messenger.bot import BotMessenger
from renewal_reminder.infrastructure.storage.csv import MembersStorageCsv


@dataclass(frozen=True)
class TelegramConfig:
    chat_id: str
    token_id: str
    base_url: Optional[str] = None

    @classmethod
    def read_from_environment(cls):
        return cls(
            chat_id=environ['TELEGRAM_CHAT_ID'],
            token_id=environ['TELEGRAM_TOKEN_ID'],
            base_url=environ.get('TELEGRAM_BASE_URL'),
        )


@dataclass(frozen=True)
class AppConfig:
    days_notice: int
    file_path: str
    log_level: str
    telegram: TelegramConfig

    @classmethod
    def read_from_environment(cls):
        return cls(
            days_notice=int(environ['APP_DAYS_NOTICE']),
            log_level=environ.get('APP_LOG_LEVEL', 'INFO'),
            file_path=environ['APP_FILE_PATH'],
            telegram=TelegramConfig.read_from_environment(),
        )


def main():
    config = AppConfig.read_from_environment()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=config.log_level)

    messenger = BotMessenger(token_id=config.telegram.token_id, chat_id=config.telegram.chat_id,
                             base_url=config.telegram.base_url)
    members_storage = MembersStorageCsv(file_path=config.file_path)
    checker = RenewalChecker(messenger=messenger, members_storage=members_storage)

    checker.run(days_notice=config.days_notice)


if __name__ == '__main__':
    main()
