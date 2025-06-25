from unittest import TestCase
from gchat_sdk.controllers.chat_controller import ChatController
from gchat_sdk.tests.utils import (
    ProviderMagicMock, 
    get_limit_date_1
)

 
class ChatControllerErrorTestCase(TestCase):

    
    def test_finish_with_last_contact_message_chats(self):
        provider = ProviderMagicMock()
        provider._chat_data = {
            'chats': [
                {
                    'attendanceId': '685bde445f164d81562fc196', 
                    'contact': {
                        'id':'6569d66fa3544ba92d2f0cf3',
                        'number':'5511997799298',
                        'name':'Tatianno Alves'
                    },
                    'lastMessage': {
                        'utcDhMessage': '2025-06-25T09:56:56.274', 
                        'text': '🔼 Bom dia', 
                        'sender': {
                            'isMe': False
                        }
                    }
                }
            ]
        }
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date_1
        ) 
        result = controller.finish_chats(
            end_attendants_last_message=True,
            end_contacts_last_message=False,
            timeout=0.1
        )
        self.assertEqual(len(result['success']), 0)
        self.assertEqual(len(result['fail']), 0)

    def test_no_finish_with_last_attendant_message_chats(self):
        provider = ProviderMagicMock()
        provider._chat_data = {
            'chats': [
                {
                    'attendanceId': '685bde445f164d81562fc196', 
                    'contact': {
                        'id':'6569d66fa3544ba92d2f0cf3',
                        'number':'5511997799298',
                        'name':'Tatianno Alves'
                    },
                    'lastMessage': {
                        'utcDhMessage': '2025-06-25T09:56:56.274', 
                        'text': '🔼 Bom dia', 
                        'sender': {
                            'isMe': True
                        }
                    }
                }
            ]
        }
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date_1
        ) 
        result = controller.finish_chats(
            end_attendants_last_message=True,
            end_contacts_last_message=False,
            timeout=0.1,
            discard_not_alert_message=True
        )
        self.assertEqual(len(result['success']), 0)
        self.assertEqual(len(result['fail']), 0)
    
    def test_finish_with_last_attendant_alert_message_chats(self):
        provider = ProviderMagicMock()
        provider._chat_data = {
            'chats': [
                {
                    'attendanceId': '685bde445f164d81562fc196', 
                    'contact': {
                        'id':'6569d66fa3544ba92d2f0cf3',
                        'number':'5511997799298',
                        'name':'Tatianno Alves'
                    },
                    'lastMessage': {
                        'utcDhMessage': '2025-06-25T09:56:56.274', 
                        'text': '🔼 Você ainda está aí?', 
                        'sender': {
                            'isMe': True
                        }
                    }
                }
            ]
        }
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date_1
        ) 
        result = controller.finish_chats(
            end_attendants_last_message=True,
            end_contacts_last_message=False,
            timeout=0.1,
            discard_not_alert_message=True
        )
        self.assertEqual(len(result['success']), 1)
        self.assertEqual(len(result['fail']), 0)