from datetime import datetime, timedelta, date
from unittest.mock import Mock

import pytest
from tabulate import tabulate

from renewal_reminder.business_logic.checker import RenewalChecker
from renewal_reminder.business_logic.model.member import Member


class TestChecker:
    @pytest.fixture
    def mock_messenger(self):
        return Mock()

    @pytest.fixture
    def mock_members_retriever(self):
        return Mock()

    @pytest.fixture
    def mock_logger(self):
        return Mock()

    @pytest.fixture
    def checker(self, mock_messenger, mock_members_retriever, mock_logger):
        yield RenewalChecker(messenger=mock_messenger, members_retriever=mock_members_retriever)

    @pytest.mark.parametrize('members, expected', [
        ([Member(name='person1', grade='9 kyu', licence_expiry=datetime.now().date())], True),
        ([], True),
    ], ids=repr)
    def test_run_with_messenger_send_called(self, checker, mock_members_retriever, mock_messenger, members, expected):
        mock_members_retriever.get.return_value = members

        checker.run(days_notice=1)
        actual = mock_messenger.send.called
        assert actual == expected

    @pytest.mark.parametrize('days_notice, members, expected', [
        (
            1,
            [],
            {
                'msg': 'No renewals due.'
            },
        ),
        (
            2,
            [Member(name='person', grade='9 kyu', licence_expiry=datetime.strptime('01-01-2018', '%d-%m-%Y').date())],
            {
                'msg': 'There is 1 renewals due in the next 2 day(s). Due on 01-01-2018.'
            },
        ),
        (
            3,
            [
                Member(name='person1', grade='9 kyu', licence_expiry=datetime.strptime('05-06-2019', '%d-%m-%Y').date()),
                Member(name='person2', grade='8 kyu', licence_expiry=datetime.strptime('03-03-2018', '%d-%m-%Y').date()),
                Member(name='person3', grade='7 kyu', licence_expiry=datetime.strptime('01-01-2018', '%d-%m-%Y').date()),
            ],
            {
                'msg': 'There are 3 renewals due in the next 3 day(s). Closest due on 01-01-2018.'
            }
        ),
    ], ids=repr)
    def test_run_with_messenger_send_messages(self, checker, mock_members_retriever, mock_messenger, days_notice,
                                              members, expected):
        mock_members_retriever.get.return_value = members
        checker.run(days_notice=days_notice)

        if expected['msg'] != 'No renewals due.':
            msg = expected['msg']
            members = [[member.name, member.grade, member.licence_expiry] for member in members]
            table = tabulate(members, headers=['Name', 'Grade', 'Licence Expiry'], tablefmt='orgtbl')
            expected['msg'] = f'{msg}\n\n{table}'

        mock_messenger.send.assert_called_with(**expected)

    def test__check(self, checker):
        member1 = Mock()
        member1.licence_expiry = datetime.now().date() + timedelta(+0)
        member2 = Mock()
        member2.licence_expiry = datetime.now().date() + timedelta(-1)
        member3 = Mock()
        member3.licence_expiry = datetime.now().date() + timedelta(+2)
        member4 = Mock()
        member4.licence_expiry = None

        members = [member1, member2, member3, member4]

        expected = [member1, member2]
        actual = checker._check(members=members, days_notice=datetime.now().date())
        assert actual == expected
