from datetime import datetime, timedelta
from typing import List

from renewal_reminder.business_logic.model.member import Member
from renewal_reminder.ports.renewal import RenewalChecker


class RenewalCheckerNotice(RenewalChecker):
    def __init__(self, days_notice: int):
        self._notice_date = datetime.now().date() + timedelta(+days_notice)

    def check(self, members: List[Member]) -> List[Member]:
        renewals_due: List[Member] = []
        for member in members:
            if member.licence_expiry and self._notice_date >= member.licence_expiry:
                renewals_due.append(member)

        return renewals_due
