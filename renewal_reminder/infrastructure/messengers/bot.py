from typing import NoReturn

from telegram import Bot

from renewal_reminder.ports.ports import Messenger


class BotMessenger(Messenger):
    def __init__(self, token_id: str):
        self.bot = Bot(token=token_id)

    def send(self, msg: str, *arg, **kwargs) -> NoReturn:
        chat_id = kwargs['chat_id']
        self.bot.sendMessage(chat_id=chat_id, text=msg)
        # self.logger.info(f'These are the dates due for renewal: {renewal_dates}')
