from datetime import datetime
from unittest.mock import Mock

import pytest

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

    @pytest.mark.parametrize('renewal_dates, expected',
                             [([datetime.now().date()], True),
                              ([], False),
                              ], ids=repr)
    def test_run_with_messenger_send_called(self, checker, mock_messenger, mock_renewals, renewal_dates, expected):
        mock_renewals.get.return_value = renewal_dates
        checker.run(chat_id='chat_id')

        actual = mock_messenger.send.called

        assert actual == expected

    @pytest.mark.parametrize('chat_id, renewal_dates, expected',
                             [('chat_id1', ['01-01-2018'], {
                                 'chat_id': 'chat_id1',
                                 'msg': 'There is 1 renewals due in the next 30 days. Due on 01-01-2018.'}),
                              ('chat_id2', ['05-06-2019', '03-03-2018', '01-01-2018'], {
                                  'chat_id': 'chat_id2',
                                  'msg': 'There are 3 renewals due in the next 30 days. Closest due on 01-01-2018.'}),
                              ], ids=repr)
    def test_run_with_messenger_send_messages(self, checker, mock_messenger, mock_renewals, chat_id, renewal_dates,
                                              expected):
        mock_renewals.get.return_value = renewal_dates
        checker.run(chat_id=chat_id)

        mock_messenger.send.assert_called_with(**expected)
