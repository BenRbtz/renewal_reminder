from datetime import date
from typing import List

from renewal_reminder.business_logic.model.member import Member


class RenewalChecker:
    def check(self, days_notice: date, members: List[Member]) -> List[Member]:
        """ Get members that are due a renewal """
