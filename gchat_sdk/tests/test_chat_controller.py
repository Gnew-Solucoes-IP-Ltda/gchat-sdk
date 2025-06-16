from unittest import TestCase
from gchat_sdk.controllers.chat_controller import ChatController
from gchat_sdk.tests.utils import (
    ProviderMagicMock, 
    ProviderSendMessageMagicMock, 
    ProviderSendMessageWithAlertMagicMock, 
    ProviderSendMessageWithAlertExceptionContactMagicMock,
    get_limit_date
)

 
class ChatControllerTestCase(TestCase):

    def test_get_manual_open_chats(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date
        )
        chats = controller.get_manual_open_chats()
        self.assertEqual(len(chats), 4)
    
    def test_get_chats_without_response(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date
        ) 
        chats = controller.get_chats_without_response(value_time=2, is_me=False)
        self.assertEqual(len(chats), 1)
    
    def test_get_chats_without_response_is_me(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date
        ) 
        chats = controller.get_chats_without_response(value_time=2, is_me=True)
        self.assertEqual(len(chats), 1)
    
    def test_finish_chats(self):
        provider = ProviderMagicMock()
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date
        ) 
        result = controller.finish_chats(
            end_attendants_last_message=False,
            end_contacts_last_message=True,
            timeout=2
        )
        self.assertEqual(len(result['success']), 1)
        self.assertEqual(len(result['fail']), 0)
    
    def test_alert_chats(self):
        provider = ProviderSendMessageMagicMock()
        controller = ChatController(
            provider,
            'voce ainda esta ai',
            get_limit_date
        )     
        result = controller.alert_chats(alert_time_in_hour=0.1) 
        self.assertEqual(len(result['success']), 1)
        self.assertEqual(len(result['fail']), 0)
    
    def test_alert_chats_with_send_alert_message(self):
        provider = ProviderSendMessageWithAlertMagicMock()
        controller = ChatController(
            provider,
            'Voce ainda esta ai',
            get_limit_date
        )    
        result = controller.alert_chats(alert_time_in_hour=0.1)         
        self.assertEqual(len(result['success']), 0)
        self.assertEqual(len(result['fail']), 0)
    
    def test_alert_chats_with_send_alert_message_exception_contact(self):
        provider = ProviderSendMessageWithAlertExceptionContactMagicMock()
        controller = ChatController(
            provider,
            'Você ainda está aí?',
            get_limit_date
        )  
        controller._test_contact_id = '6569d66fa3544ba92d2f0cf3'
        result = controller.alert_chats(alert_time_in_hour=0.1) 
        self.assertEqual(len(result['success']), 1)
        self.assertEqual(len(result['fail']), 0)