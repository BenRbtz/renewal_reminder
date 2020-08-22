from csv import DictReader
from datetime import datetime
from typing import List

from renewal_reminder.business_logic.members import Member
from renewal_reminder.ports.storage import MembersRetriever


FIELDS = {'name', 'grade', 'licence expiry'}


class CsvMembersRetriever(MembersRetriever):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get(self) -> List[Member]:
        with open(file=self.file_path, mode='r', encoding='utf-8') as file:
            reader = DictReader(f=file)

            data = file.read()
            if not data:
                raise ValueError(f'No data in csv {self.file_path}')
            file.seek(0)  # Resets reader

            if not FIELDS.issubset(set(reader.fieldnames)):
                raise KeyError('CSV fieldnames not match expected fieldnames')

            members: List[Member] = []
            for row in reader:
                if not row['licence expiry']:
                    continue
                date = datetime.strptime(row['licence expiry'], "%d-%m-%Y").date()
                members.append(Member(name=row['name'], grade=row['grade'], licence_expiry=date))

        return members
