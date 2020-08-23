import logging
from typing import Optional

from telegram import Bot

from renewal_reminder.ports.messenger import Messenger


class BotMessenger(Messenger):
    def __init__(self, token_id: str, chat_id: str, base_url: Optional[str] = None):
        self._bot = Bot(token=token_id, base_url=base_url)
        self._chat_id = chat_id

    def send(self, msg: str) -> None:
        logging.info('Message being sent: %s', msg)
        self._bot.send_message(chat_id=self._chat_id, text=msg)
