from unittest import TestCase
from controllers import ChatController
from .utils import ProviderMagicMock, get_limit_date

 
class ChatControllerTestCase(TestCase):

    def test_get_manual_open_chats(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            get_limit_date
        ) 
        chats = controller.get_manual_open_chats()
        self.assertEqual(len(chats), 14)
    
    def test_get_chats_without_response(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            get_limit_date
        ) 
        chats = controller.get_chats_without_response(value_time=2, is_me=False)
        self.assertEqual(len(chats), 6)
    
    def test_get_chats_without_response_is_me(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            get_limit_date
        ) 
        chats = controller.get_chats_without_response(value_time=2, is_me=True)
        self.assertEqual(len(chats), 8)
    
    def test_finish_chats(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            get_limit_date
        ) 
        result = controller.finish_chats(
            end_attendants_last_message=False,
            end_contacts_last_message=True,
            timeout=2
        )
        self.assertEqual(len(result['success']), 5)
        self.assertEqual(len(result['fail']), 1)