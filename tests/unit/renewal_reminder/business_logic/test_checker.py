from datetime import datetime
from unittest.mock import Mock

import pytest
from tabulate import tabulate

from renewal_reminder.business_logic.model.member import Member
from renewal_reminder.business_logic.checker import Checker


class TestChecker:
    @pytest.fixture()
    def mock_messenger(self):
        return Mock()

    @pytest.fixture()
    def mock_renewal_checker(self):
        return Mock()

    @pytest.fixture()
    def mock_members_retriever(self):
        return Mock()

    @pytest.fixture()
    def mock_logger(self):
        return Mock()

    @pytest.fixture()
    def checker(self, mock_messenger, mock_renewal_checker, mock_members_retriever, mock_logger):
        yield Checker(messenger=mock_messenger, renewal_checker=mock_renewal_checker,
                      members_retriever=mock_members_retriever)

    @pytest.mark.parametrize('members, expected',
                             [([Member(name='person1', grade='9 kyu', licence_expiry=datetime.now().date())], True),
                              ([], True),
                              ], ids=repr)
    def test_run_with_messenger_send_called(self, checker, mock_messenger, mock_renewal_checker, members, expected):
        mock_renewal_checker.check.return_value = members
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
                [Member(name='person', grade='9 kyu', licence_expiry='01-01-2018')],
                {
                    'msg': 'There is 1 renewals due in the next 2 day(s). Due on 01-01-2018.'
                },
        ),
        (
                3,
                [
                    Member(name='person1', grade='9 kyu', licence_expiry='05-06-2019'),
                    Member(name='person2', grade='8 kyu', licence_expiry='03-03-2018'),
                    Member(name='person3', grade='7 kyu', licence_expiry='01-01-2018'),
                ],
                {
                    'msg': 'There are 3 renewals due in the next 3 day(s). Closest due on 01-01-2018.'
                }
        ),
    ], ids=repr)
    def test_run_with_messenger_send_messages(self, checker, mock_messenger, mock_renewal_checker, days_notice, members,
                                              expected):
        mock_renewal_checker.check.return_value = members
        checker.run(days_notice=days_notice)

        if expected['msg'] != 'No renewals due.':
            msg = expected['msg']
            members = [[member.name, member.grade, member.licence_expiry] for member in members]
            table = tabulate(members, headers=['Name', 'Grade', 'Licence Expiry'], tablefmt='orgtbl')
            expected['msg'] = f'{msg}\n\n{table}'

        mock_messenger.send.assert_called_with(**expected)
