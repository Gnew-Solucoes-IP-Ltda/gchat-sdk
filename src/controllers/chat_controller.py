from entities import Chat
from factories import get_chat_instance
from providers.chatbot_provider import ChatBotProvider
from settings import ALERT_MESSAGE_TEXT, TEST_CONTACT_ID
from utils import get_limit_date


class ChatController:
    _test_contact_id = TEST_CONTACT_ID
    
    def __init__(
        self, 
        chatbot_provider: ChatBotProvider, 
        func_get_limit_date: callable=get_limit_date
    ):
        self._chatbot_provider = chatbot_provider
        self._get_limit_date = func_get_limit_date
    
    def get_chats_without_response(self, value_time: int, is_me=True, alert_message=False, page=1) -> list[Chat]:
        response_date_limit = self._get_limit_date(value_time)
        chats = []
        
        for chat in self.get_manual_open_chats(page):
            contact = chat.contact
            
            if chat.is_me == is_me and chat.last_message_date < response_date_limit:
                if alert_message and  ALERT_MESSAGE_TEXT in chat.last_message:
                    continue
                
                if self._test_contact_id:
                    if contact.id != self._test_contact_id:
                        continue
                
                chats.append(chat)

        return chats

    def get_manual_open_chats(self, page=1) -> list[Chat]:
        response = self._chatbot_provider.get_chats(status=2, type_chat=1, page=page)
        chats = []
        
        if response.status_code == 200:
            for data in response.json().get('chats', []):
                chats.append(get_chat_instance(data))

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
        return chats
    
    def alert_chats(self, alert_time_in_hour: int) -> dict:
        chats = []
        request_executed = False
        result = {'success': [], 'fail': []}
        page = 1
        
        while request_executed == False:
            chats_without_response = self.get_chats_without_response(
                value_time=alert_time_in_hour, 
                is_me=True, 
                alert_message=True, 
                page=page
            )
            chats.extend(
                chats_without_response
            )
            page += 1

            if len(chats_without_response) == 0:
                request_executed = True

        data = self._send_message(chats)
        result['success'].extend(data['success'])
        result['fail'].extend(data['fail'])
        return result
                
    def finish_chats(self, end_attendants_last_message: bool, end_contacts_last_message: bool, timeout: int) -> dict:
        chats = []
        request_executed = False
        result = {'success': [], 'fail': []}

        while len(chats) != 0 or request_executed == False:

            if end_attendants_last_message:
                chats.extend(self.get_chats_without_response(value_time=timeout, is_me=True))
            
            if end_contacts_last_message:
                chats.extend(self.get_chats_without_response(value_time=timeout, is_me=False))
            
            data = self._finish_chats(chats)
            result['success'].extend(data['success'])
            result['fail'].extend(data['fail'])
            
            if len(chats) == 0:
                request_executed = True

            chats = []
            
        return result

    def _finish_chats(self, chats: list[Chat]) -> dict:
        sucess = []
        fail = []

        for chat in chats:              
            response = self._chatbot_provider.finish_chat(chat.id)
            
            if response.status_code == 200:
                sucess.append(chat.id)
            
            else:
                fail.append(chat.id)
            
        return {    
            'success': sucess,
            'fail': fail
        }
    
    def _send_message(self, chats: list[Chat]) -> dict:
        sucess = []
        fail = []
        message = ALERT_MESSAGE_TEXT

        for chat in chats:            
            contact = chat.contact  
            response = self._chatbot_provider.send_message(contact.id, message)
            
            if response.status_code == 202:
                sucess.append(chat.id)
            
            else:
                fail.append(chat.id)
            
        return {    
            'success': sucess,
            'fail': fail
        }
