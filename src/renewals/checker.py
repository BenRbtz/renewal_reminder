import csv
from datetime import datetime, timedelta


def open_file(func):
    def _open_file(self, filename, *args):
        with open(filename) as file:
            data = file.read()
            if not data:
                raise ValueError(f'No data in csv {filename}')
            file.seek(0)
            return func(self, file, *args)

    return _open_file


class Checker:
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    def run(self, chat_id, file_path, renewal_notice_days=30):
        self.logger.info('Renewal Checker Started')

        renewal_notice_date = datetime.now().date() + timedelta(+renewal_notice_days)
        renewal_dates = self._get_renewal_dates(file_path, renewal_notice_date)

        if renewal_dates:
            self.logger.info(f'These are the dates due for renewal: {renewal_dates}')
            msg = self._get_renewal_message(renewal_dates)
            self._send(chat_id, msg)

        self.logger.info('Renewal Checker Finished')

    @open_file
    def _get_renewal_dates(self, file, renewal_notice_date):
        reader = csv.reader(file)
        columns = next(reader)

        try:
            license_exp_ind = columns.index("licence expiry")
        except ValueError:
            raise ValueError("No column 'licence expiry' exists in file")

        renewals_due = []
        for row in reader:
            if not row:
                continue

            expiry_date_str = row[license_exp_ind]

            if self._check_date_expired(renewal_notice_date, expiry_date_str):
                renewals_due.append(expiry_date_str)

        return renewals_due

    @staticmethod
    def _check_date_expired(renewal_notice_date, expiry_date_str):
        if not expiry_date_str:
            return False

        expire_date = datetime.strptime(expiry_date_str, '%d-%m-%Y').date()
        return renewal_notice_date >= expire_date

    @staticmethod
    def _get_renewal_message(renewal_dates):
        date_counts = len(renewal_dates)
        oldest_date = min(renewal_dates)

        msg = f'There is {date_counts} karate_project due in the next 30 days. Due on {oldest_date}.'
        if len(renewal_dates) > 1:
            msg = f'There are {date_counts} karate_project due in the next 30 days. Closest due on {oldest_date}.'

        return msg

    def _send(self, chat_id, msg):
        self.bot.sendMessage(chat_id=chat_id, text=msg)
