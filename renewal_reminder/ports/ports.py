from typing import List, NoReturn

from renewal_reminder.business_logic.members import Member


class Messenger:
    def send(self, msg: str, *arg, **kwargs) -> NoReturn:
        pass


class MembersRetriever:
    def get(self) -> List[Member]:
        pass
