from datetime import date, datetime, timedelta
from typing import Optional, List

from renewal_reminder.business_logic.model.member import Member


class Renewals:
    def __init__(self, days_notice: int):
        self.notice_date = datetime.now().date() + timedelta(+days_notice)

    def get(self, members: List[Member]) -> List[Member]:
        renewals_due: List[Member] = []
        for member in members:
            if self._check_date_expired(expiry_date=member.licence_expiry):
                renewals_due.append(member)

        return renewals_due

    def _check_date_expired(self, expiry_date: Optional[date] = None) -> bool:
        if not expiry_date:
            return False

        return self.notice_date >= expiry_date
