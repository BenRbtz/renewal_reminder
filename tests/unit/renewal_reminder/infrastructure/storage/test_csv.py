from datetime import datetime, timedelta

import pytest

from renewal_reminder.business_logic.model.member import Member
from renewal_reminder.infrastructure.storage.csv import CsvMembersRetriever


@pytest.fixture()
def file(tmpdir):
    def _file(content: str = ''):
        csv_file = tmpdir.join('file.csv')
        csv_file.write(content)

        return str(csv_file)

    return _file


class TestCsvMembersRetriever:
    def test_get_with_members(self, file):
        dates = [
            (datetime.now() + timedelta(+0)).date(),
            (datetime.now() + timedelta(+1)).date(),
            (datetime.now() + timedelta(+2)).date(),
        ]
        csv_content = 'name,grade,licence expiry\n,,\n'
        expected = []
        for date in dates:
            date_format = date.strftime('%d-%m-%Y')
            csv_content += f'person,10 kyu,{date_format}\n'
            expected.append(Member(name='person', grade='10 kyu', licence_expiry=date))
        file_path = file(content=csv_content)

        actual = CsvMembersRetriever(file_path=file_path).get()

        assert actual == expected

    def test_get_with_csv_empty(self, file):
        file_path = file()

        with pytest.raises(ValueError) as exception:
            CsvMembersRetriever(file_path=file_path).get()

        assert 'No data in csv' in str(exception.value)

    def test_get_with_licence_expiry_column_not_exist(self, file):
        csv_content = "name,grade,\n"
        csv_file = file(content=csv_content)

        with pytest.raises(KeyError) as exception:
            CsvMembersRetriever(file_path=str(csv_file)).get()

        assert "CSV fieldnames not match expected fieldnames" in str(exception.value)
