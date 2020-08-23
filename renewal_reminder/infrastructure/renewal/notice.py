from datetime import date
from typing import List

from renewal_reminder.business_logic.model.member import Member
from renewal_reminder.ports.renewal import RenewalChecker


class RenewalCheckerNotice(RenewalChecker):
    def check(self, days_notice: date, members: List[Member]) -> List[Member]:
        renewals_due: List[Member] = []
        for member in members:
            if member.licence_expiry and days_notice >= member.licence_expiry:
                renewals_due.append(member)

        return renewals_due
