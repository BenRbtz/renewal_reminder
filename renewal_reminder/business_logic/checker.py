import logging
from datetime import timedelta, datetime, date
from typing import List, Optional

from tabulate import tabulate

from renewal_reminder.business_logic.model.member import Member
from renewal_reminder.ports.messenger import Messenger
from renewal_reminder.ports.storage import MembersRetriever


class RenewalChecker:

    def __init__(self, messenger: Messenger, members_retriever: MembersRetriever):
        self._messenger = messenger
        self._members_retriever = members_retriever

    def run(self, days_notice: int) -> None:
        days_notice_as_date = datetime.now().date() + timedelta(+days_notice)

        logging.info(msg='Start check for _renewal_checker')
        members = self._members_retriever.get()
        members_due_renewal = self._check(members=members, days_notice=days_notice_as_date)
        msg = self._prepare_message(days_notice=days_notice, members_due_renewals=members_due_renewal)

        self._messenger.send(msg=msg)

    @staticmethod
    def _check(days_notice: date, members: List[Member]) -> List[Member]:
        renewals_due: List[Member] = []
        for member in members:
            if member.licence_expiry and days_notice >= member.licence_expiry:
                renewals_due.append(member)

        return renewals_due

    @staticmethod
    def _prepare_message(days_notice: int,
                         members_due_renewals: List[Member]) -> Optional[str]:
        if not members_due_renewals:
            return 'No renewals due.'

        date_counts = len(members_due_renewals)
        first_member_licence_due = min(members_due_renewals, key=lambda x: x.licence_expiry)
        licence_expiry = first_member_licence_due.licence_expiry.strftime('%d-%m-%Y')

        msg = (f'There is {date_counts} renewals due in the next {days_notice} day(s). '
               f'Due on {licence_expiry}.')
        if len(members_due_renewals) > 1:
            msg = (f'There are {date_counts} renewals due in the next {days_notice} day(s). '
                   f'Closest due on {licence_expiry}.')

        members = [
            [member.name, member.grade, member.licence_expiry]
            for member in members_due_renewals
        ]
        table = tabulate(members, headers=['Name', 'Grade', 'Licence Expiry'], tablefmt='orgtbl')
        msg = f'{msg}\n\n{table}'

        return msg
