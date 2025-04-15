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
        chats = controller.get_chats_without_response(hours=2, is_me=False)
        self.assertEqual(len(chats), 6)
    
    def test_get_chats_without_response_is_me(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            get_limit_date
        ) 
        chats = controller.get_chats_without_response(hours=2, is_me=True)
        self.assertEqual(len(chats), 8)
    
    def test_finalize_chats(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            get_limit_date
        ) 
        chats = controller.get_chats_without_response(hours=2, is_me=False)
        result = controller.finalize_chats(chats)
        self.assertEqual(len(result['success']), 5)
        self.assertEqual(len(result['fail']), 1)