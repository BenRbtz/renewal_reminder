from datetime import datetime
from unittest.mock import Mock

import pytest
from tabulate import tabulate

from renewal_reminder.business_logic.members import Member
from renewal_reminder.ports.checker import Checker


class TestChecker:
    @pytest.fixture()
    def mock_messenger(self):
        return Mock()

    @pytest.fixture()
    def mock_renewals(self):
        return Mock()

    @pytest.fixture()
    def mock_members_retriever(self):
        return Mock()

    @pytest.fixture()
    def mock_logger(self):
        return Mock()

    @pytest.fixture()
    def checker(self, mock_messenger, mock_renewals, mock_members_retriever, mock_logger):
        yield Checker(messenger=mock_messenger, renewals=mock_renewals, members_retriever=mock_members_retriever,
                      logger=mock_logger)

    @pytest.mark.parametrize('members, expected',
                             [([Member(name='person1', grade='9 kyu', licence_expiry=datetime.now().date())], True),
                              ([], True),
                              ], ids=repr)
    def test_run_with_messenger_send_called(self, checker, mock_messenger, mock_renewals, members, expected):
        mock_renewals.get.return_value = members
        checker.run(chat_id='chat_id')
        actual = mock_messenger.send.called
        assert actual == expected

    @pytest.mark.parametrize('chat_id, members, expected', [
        (
                'chat_id1',
                [],
                {
                    'chat_id': 'chat_id1',
                    'msg': 'No renewals due.'
                },
        ),
        (
                'chat_id1',
                [Member(name='person', grade='9 kyu', licence_expiry='01-01-2018')],
                {
                    'chat_id': 'chat_id1',
                    'msg': 'There is 1 renewals due in the next 30 days. Due on 01-01-2018.'
                },
        ),
        (
                'chat_id2',
                [
                    Member(name='person1', grade='9 kyu', licence_expiry='05-06-2019'),
                    Member(name='person2', grade='8 kyu', licence_expiry='03-03-2018'),
                    Member(name='person3', grade='7 kyu', licence_expiry='01-01-2018'),
                ],
                {
                    'chat_id': 'chat_id2',
                    'msg': 'There are 3 renewals due in the next 30 days. Closest due on 01-01-2018.'
                }
        ),
    ], ids=repr)
    def test_run_with_messenger_send_messages(self, checker, mock_messenger, mock_renewals, chat_id, members,
                                              expected):
        mock_renewals.get.return_value = members
        checker.run(chat_id=chat_id)

        if expected['msg'] != 'No renewals due.':
            msg = expected['msg']
            members = [[member.name, member.grade, member.licence_expiry] for member in members]
            table = tabulate(members, headers=['Name', 'Grade', 'Licence Expiry'], tablefmt='orgtbl')
            expected['msg'] = f'{msg}\n\n{table}'

        mock_messenger.send.assert_called_with(**expected)
