from datetime import datetime, timedelta
from unittest.mock import Mock

from renewal_reminder.infrastructure.renewals import Renewals


class TestRenewals:
    def test_get_with_some_dates_returned(self):
        member1 = Mock()
        member1.licence_expiry = datetime.now().date() + timedelta(+0)
        member2 = Mock()
        member2.licence_expiry = datetime.now().date() + timedelta(+1)
        member3 = Mock()
        member3.licence_expiry = datetime.now().date() + timedelta(+2)
        member4 = Mock()
        member4.licence_expiry = None

        members = [member1, member2, member3, member4]

        expected = [member1.licence_expiry, member2.licence_expiry]
        actual = Renewals(notice_days=1).get(members=members)
        assert actual == expected
