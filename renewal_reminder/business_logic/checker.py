import logging
from typing import List, Optional

from tabulate import tabulate

from renewal_reminder.business_logic.model.member import Member
from renewal_reminder.ports.messenger import Messenger
from renewal_reminder.ports.renewal import RenewalChecker
from renewal_reminder.ports.storage import MembersRetriever


class Checker:
    def __init__(self, messenger: Messenger, renewal_checker: RenewalChecker,
                 members_retriever: MembersRetriever):
        self._messenger = messenger
        self._renewal_checker = renewal_checker
        self._members_retriever = members_retriever

    def run(self) -> None:
        logging.info(msg='Start check for _renewal_checker')
        members = self._members_retriever.get()
        members_due_renewal = self._renewal_checker.check(members=members)
        msg = self._get_renewal_message(members_due_renewal)

        self._messenger.send(msg=msg)

    @staticmethod
    def _get_renewal_message(members_due_renewals: List[Member]) -> Optional[str]:
        if not members_due_renewals:
            return 'No renewals due.'

        date_counts = len(members_due_renewals)
        first_member_licence_due = min(members_due_renewals, key=lambda x: x.licence_expiry)

        msg = (f'There is {date_counts} renewals due in the next 30 days. '
               f'Due on {first_member_licence_due.licence_expiry}.')
        if len(members_due_renewals) > 1:
            msg = (f'There are {date_counts} renewals due in the next 30 days. '
                   f'Closest due on {first_member_licence_due.licence_expiry}.')

        members = [
            [member.name, member.grade, member.licence_expiry]
            for member in members_due_renewals
        ]
        table = tabulate(members, headers=['Name', 'Grade', 'Licence Expiry'], tablefmt='orgtbl')
        msg = f'{msg}\n\n{table}'

        return msg
