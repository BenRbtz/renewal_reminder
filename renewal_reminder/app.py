import logging

from renewal_reminder.config import get_config
from renewal_reminder.infrastructure.members_retriever.csv import CsvMembersRetriever
from renewal_reminder.infrastructure.messengers.bot import BotMessenger
from renewal_reminder.infrastructure.renewals import Renewals
from renewal_reminder.ports.checker import Checker


def main():
    config = get_config()

    # logging.basicConfig(level=logging.DEBUG,
    #                     filename=log_path,
    #                     filemode='w',
    #                     format='%(asctime)s - %(levelname)s - %(message)s',
    #                     datefmt='%d-%b-%y %H:%M:%S')

    messenger = BotMessenger(token_id=config.token_id)
    renewals = Renewals(notice_days=config.notice_days)
    members_retriever = CsvMembersRetriever(file_path=config.file_path)
    checker = Checker(messenger=messenger, renewals=renewals, members_retriever=members_retriever, logger=logging)

    checker.run(chat_id=config.chat_id)


if __name__ == '__main__':
    main()
