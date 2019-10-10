from datetime import date, datetime, timedelta
from typing import Optional, List

from renewal_reminder.business_logic.members import Member


class Renewals:
    def __init__(self, notice_days: int):
        self.notice_date = datetime.now().date() + timedelta(+notice_days)

    def get(self, members: List[Member]) -> List[date]:
        renewals_due: List[date] = []
        for member in members:
            if self._check_date_expired(expiry_date=member.licence_expiry):
                renewals_due.append(member.licence_expiry)

        return renewals_due

    def _check_date_expired(self, expiry_date: Optional[date] = None):
        if not expiry_date:
            return False

        return self.notice_date >= expiry_date