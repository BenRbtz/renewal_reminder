from unittest.mock import patch, Mock

from renewal_reminder.infrastructure.messenger.bot import BotMessenger


class TestBotMessenger:
    @patch('renewal_reminder.infrastructure.messenger.bot.Bot')
    def test_send(self, mock_bot):
        mock_bot_ins = Mock()
        mock_bot.return_value = mock_bot_ins
        BotMessenger(token_id='token_id', chat_id='chat_id').send(msg='test msg')
        mock_bot_ins.send_message.assert_called_with(chat_id='chat_id', text='test msg')
