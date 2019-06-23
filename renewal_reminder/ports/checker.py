import logging
from datetime import date
from typing import List, Optional

from renewal_reminder.infrastructure.renewals import Renewals
from renewal_reminder.ports.ports import Messenger, MembersRetriever


class Checker:
    def __init__(self, messenger: Messenger, renewals: Renewals, members_retriever: MembersRetriever, logger: logging):
        self.messenger = messenger
        self.renewals = renewals
        self.members_retriever = members_retriever
        self.logger = logger

    def run(self, chat_id: str):
        self.logger.info(msg='Start Check For Renewals.')
        members = self.members_retriever.get()
        renewal_dates = self.renewals.get(members=members)
        msg = self._get_renewal_message(renewal_dates)

        if msg:
            self.messenger.send(chat_id=chat_id, msg=msg)
            self.logger.info(msg=msg)
        self.logger.info(msg='Finished Check For Renewals.')

    @staticmethod
    def _get_renewal_message(renewals: List[date]) -> Optional[str]:
        if not renewals:
            return None

        date_counts = len(renewals)
        oldest_date = min(renewals)

        msg = f'There is {date_counts} renewals due in the next 30 days. Due on {oldest_date}.'
        if len(renewals) > 1:
            msg = f'There are {date_counts} renewals due in the next 30 days. Closest due on {oldest_date}.'

        return msg
