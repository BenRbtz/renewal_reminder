import logging
from dataclasses import dataclass
from os import environ
from typing import Optional

from renewal_reminder.business_logic.checker import Checker
from renewal_reminder.infrastructure.messenger.bot import BotMessenger
from renewal_reminder.infrastructure.renewal.notice import RenewalCheckerNotice
from renewal_reminder.infrastructure.storage.csv import CsvMembersRetriever


@dataclass(frozen=True)
class Telegram:
    base_url: Optional[str] = None

    @classmethod
    def read_from_environment(cls):
        return cls(
            base_url=environ.get('TELEGRAM_BASE_URL'),
        )


@dataclass(frozen=True)
class AppConfig:
    file_path: str
    log_level: str
    token_id: str
    chat_id: str
    days_notice: int
    telegram: Telegram

    @classmethod
    def read_from_environment(cls):
        return cls(
            file_path=environ['APP_FILE_PATH'],
            log_level=environ.get('APP_LOG_LEVEL', 'INFO'),
            token_id=environ['APP_TOKEN_ID'],
            chat_id=environ['APP_CHAT_ID'],
            days_notice=int(environ['APP_DAYS_NOTICE']),
            telegram=Telegram.read_from_environment(),
        )


def main():
    config = AppConfig.read_from_environment()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=config.log_level)

    messenger = BotMessenger(token_id=config.token_id, chat_id=config.chat_id, base_url=config.telegram.base_url)
    renewals = RenewalCheckerNotice(days_notice=config.days_notice)
    members_retriever = CsvMembersRetriever(file_path=config.file_path)
    checker = Checker(messenger=messenger, renewal_checker=renewals,
                      members_retriever=members_retriever)

    checker.run()


if __name__ == '__main__':
    main()
