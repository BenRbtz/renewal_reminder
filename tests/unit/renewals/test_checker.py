import logging
from collections import namedtuple
from datetime import datetime, timedelta

import pytest
import telegram

from renewals import checker

File = namedtuple('File', ['file_path', 'dates'])


class TestChecker:
    @pytest.fixture()
    def bot_mock(self, mocker):
        yield mocker.Mock(spec=telegram.Bot)

    @pytest.fixture()
    def bot_logger(self, mocker):
        yield mocker.Mock(spec=logging)

    @pytest.fixture()
    def my_checker(self, bot_mock, bot_logger):
        yield checker.Checker(bot_mock, bot_logger)

    @pytest.fixture()
    def file(self, tmpdir):
        def _file(number_of_dates):
            csv_file = tmpdir.join('file.csv')

            csv_content = ''
            if number_of_dates > 0:
                csv_content = "name,grade,licence expiry,\n"

            dates = []
            for day_offset in range(number_of_dates):
                date = (datetime.now() + timedelta(+day_offset)).strftime('%d-%m-%Y')
                dates.append(date)
                csv_content += f"person{day_offset},4 kyu,{date}\n"

            csv_file.write(csv_content)

            return File(file_path=csv_file, dates=dates)

        return _file

    @pytest.mark.parametrize('renewal_notice_days, expected',
                             [(-1, False),
                              (3, True),
                              ], ids=repr)
    def test_run(self, my_checker, file, bot_mock, renewal_notice_days, expected):
        file = file(number_of_dates=5)

        my_checker.run('chat_id', file.file_path, renewal_notice_days)

        actual = bot_mock.sendMessage.called

        assert expected == actual

    def test_get_renewal_dates(self, my_checker, file):
        file = file(number_of_dates=5)
        days = 3
        renewal_notice_date = datetime.now().date() + timedelta(+days)

        expected = file.dates[:days + 1]
        actual = my_checker._get_renewal_dates(file.file_path, renewal_notice_date)

        assert expected == actual

    def test_get_renewal_dates_when_csv_empty(self, my_checker, file):
        file = file(number_of_dates=0)

        with pytest.raises(ValueError) as exception:
            my_checker._get_renewal_dates(file.file_path)

        assert 'No data in csv' in str(exception.value)

    def test_get_renewal_dates_when_licence_expiry_column_not_exist(self, my_checker, tmpdir):
        csv_file = tmpdir.join('file.csv')
        csv_content = "name,grade,\n"
        csv_file.write(csv_content)

        dummy_date = datetime.now().date()

        with pytest.raises(ValueError) as exception:
            my_checker._get_renewal_dates(csv_file, dummy_date)

        assert "No column 'licence expiry' exists in file" in str(exception.value)

    @pytest.mark.parametrize('expiry_date_str, expect',
                             [
                                 ((datetime.now() + timedelta(+0)).strftime('%d-%m-%Y'), True),
                                 ((datetime.now() + timedelta(+1)).strftime('%d-%m-%Y'), True),
                                 ((datetime.now() + timedelta(+2)).strftime('%d-%m-%Y'), True),
                                 ((datetime.now() + timedelta(+3)).strftime('%d-%m-%Y'), False),
                                 ((datetime.now() + timedelta(+4)).strftime('%d-%m-%Y'), False),
                                 ('', False),
                             ], ids=repr)
    def test_check_date_expired(self, my_checker, expiry_date_str, expect):
        renewal_notice_date = datetime.now().date() + timedelta(+2)
        actual = my_checker._check_date_expired(renewal_notice_date, expiry_date_str)
        assert expect == actual

    @pytest.mark.parametrize('renewal_dates, expect',
                             [
                                 (['01-01-2018'],
                                  'There is 1 karate_project due in the next 30 days. Due on 01-01-2018.'),
                                 (['05-06-2019', '03-03-2018', '01-01-2018', ],
                                  'There are 3 karate_project due in the next 30 days. Closest due on 01-01-2018.'),
                             ], ids=repr)
    def test_get_renewal_message(self, my_checker, renewal_dates, expect):
        actual = my_checker._get_renewal_message(renewal_dates)
        assert expect == actual

    def test_send(self, my_checker, bot_mock):
        my_checker._send('id', 'test msg')
        bot_mock.sendMessage.assert_called_once_with(chat_id='id', text='test msg')
