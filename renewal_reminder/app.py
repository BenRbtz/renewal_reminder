from dataclasses import dataclass
from logging import getLogger
from os import environ

from renewal_reminder.business_logic.checker import Checker
from renewal_reminder.infrastructure.messenger.bot import BotMessenger
from renewal_reminder.infrastructure.renewals import Renewals
from renewal_reminder.infrastructure.storage.csv import CsvMembersRetriever

LOGGER = getLogger(__name__)


@dataclass(frozen=True)
class AppConfig:
    file_path: str
    log_level: str
    token_id: str
    chat_id: str
    notice_days: int

    @classmethod
    def read_from_environment(cls):
        return cls(
            file_path=environ['APP_FILE_PATH'],
            log_level=environ.get('APP_LOG_LEVEL', 'INFO'),
            token_id=environ['APP_TOKEN_ID'],
            chat_id=environ['APP_CHAT_ID'],
            notice_days=int(environ['APP_NOTICE_DAYS'])
        )


def main():
    config = AppConfig.read_from_environment()

    LOGGER.setLevel(config.log_level)

    messenger = BotMessenger(token_id=config.token_id, chat_id=config.chat_id)
    renewals = Renewals(notice_days=config.notice_days)
    members_retriever = CsvMembersRetriever(file_path=config.file_path)
    checker = Checker(messenger=messenger, renewals=renewals, members_retriever=members_retriever)

    checker.run()


if __name__ == '__main__':
    main()
