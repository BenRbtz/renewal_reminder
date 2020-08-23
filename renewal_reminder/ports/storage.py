from typing import List

from renewal_reminder.business_logic.model.member import Member


class MembersStorage:
    def get(self) -> List[Member]:
        """ Get members """
