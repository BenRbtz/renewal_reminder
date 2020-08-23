from csv import DictWriter
from datetime import date, timedelta
from os import environ
from tempfile import mktemp

from behave import given, when, then
from behave.runner import Context


@given('Telegram API is available')
def step_impl(context: Context):
    expected_status = 200
    actual_status = context.telegram_api_controller.health().status_code
    assert actual_status == expected_status, f'Telegram API is unavailable. ' \
                                             f'Expect status: {expected_status}. ' \
                                             f'Actual status: {actual_status}.'


@given('the file contains')
def step_impl(context: Context):
    file_path = mktemp('test_file.csv')
    print(f'File path for CSV: {file_path}')
    with open(file=file_path, mode='w', encoding='utf-8') as file:
        writer = DictWriter(f=file, fieldnames=context.table.headings)
        writer.writeheader()

        for row in context.table.rows:
            row = row.as_dict()
            licence_expiry = (date.today() + timedelta(int(row['licence expiry']))).strftime('%d-%m-%Y')
            row['licence expiry'] = licence_expiry
            writer.writerow(row)

    context.csv_file_path = file_path


@when('renewal reminder is executed with {number_of_days:d} day notice')
def step_impl(context: Context, number_of_days: int):
    from renewal_reminder.app import main

    environ['APP_DAYS_NOTICE'] = str(number_of_days)
    environ['APP_FILE_PATH'] = str(context.csv_file_path)

    main()


@then('Telegram API receives request containing "{expected_body}"')
def step_impl(context: Context, expected_body: str):
    actual_body = context.telegram_api_controller.last_request().json()['text']
    assert expected_body in actual_body, f'Unexpected Telegram API request body. ' \
                                         f'Expected: {expected_body}. ' \
                                         f'Actual: {actual_body}. '
