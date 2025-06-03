import pytz
from unittest import TestCase
from datetime import datetime
from entities import Chat
from tests.utils import contact_mock


class ChatTestCase(TestCase):
    
    def test_chat_instance(self):
        chat = Chat(
            id='67fea56f0b473cc94365c920', 
            last_message_date='2025-04-15T16:27:16', 
            is_me=False,
            contact=contact_mock
        )
        expected_date = datetime.fromisoformat('2025-04-15T16:27:16').replace(tzinfo=pytz.timezone("America/Sao_Paulo"))
        self.assertEqual(chat.id, '67fea56f0b473cc94365c920')
        self.assertEqual(chat.last_message_date, expected_date)