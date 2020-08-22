from telegram import Bot

from renewal_reminder.ports.messenger import Messenger


class BotMessenger(Messenger):
    def __init__(self, token_id: str, chat_id: str):
        self._bot = Bot(token=token_id)
        self._chat_id = chat_id

    def send(self, msg: str) -> None:
        self._bot.sendMessage(chat_id=self._chat_id, text=msg)
        # self.logger.info(f'These are the dates due for renewal: {renewal_dates}')
