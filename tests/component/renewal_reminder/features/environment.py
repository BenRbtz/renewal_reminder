from os import environ

from behave import fixture
from behave.fixture import use_fixture_by_tag
from behave.runner import Context

from tests.component.renewal_reminder.features.controller.telegram_bot import TelegramController


@fixture
def controller_telegram_api(context: Context):
    controller = TelegramController(base_url=environ['TELEGRAM_BASE_URL'])
    context.telegram_api_controller = controller

    yield controller

    controller.clear_requests()


FIXTURE_REGISTRY = {
    "fixture.controller.telegram_api": controller_telegram_api,
}


def before_all(context: Context):
    environ['APP_LOG_LEVEL'] = 'DEBUG'

    environ['TELEGRAM_CHAT_ID'] = 'chat_id'
    environ['TELEGRAM_TOKEN_ID'] = '123:abc'
    environ['TELEGRAM_BASE_URL'] = 'http://localhost:8080/'


def before_tag(context, tag):
    if tag.startswith("fixture."):
        use_fixture_by_tag(tag, context, FIXTURE_REGISTRY)
