from unittest.mock import patch, Mock

from renewal_reminder.infrastructure.messengers.bot import BotMessenger


class TestBotMessenger:
    @patch('renewal_reminder.infrastructure.messengers.bot.Bot')
    def test_send(self, mock_bot):
        mock_bot_ins = Mock()
        mock_bot.return_value = mock_bot_ins
        BotMessenger(token_id='token_id').send(chat_id='chat_id', msg='test msg')
        mock_bot_ins.sendMessage.assert_called_with(chat_id='chat_id', text='test msg')
