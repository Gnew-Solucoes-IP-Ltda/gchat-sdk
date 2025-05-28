from entities import Chat
from factories import get_chat_instance
from providers.chatbot_provider import ChatBotProvider
from utils import get_limit_date


class ChatController:

    def __init__(
        self, 
        chatbot_provider: ChatBotProvider, 
        func_get_limit_date: callable=get_limit_date
    ):
        self._chatbot_provider = chatbot_provider
        self._get_limit_date = func_get_limit_date
    
    def get_chats_without_response(self, value_time: int, is_me=True) -> list[Chat]:
        response_date_limit = self._get_limit_date(value_time)
        return [
            chat
            for chat in self.get_manual_open_chats()
            if chat.is_me == is_me and chat.last_message_date < response_date_limit
        ] 

    def get_manual_open_chats(self) -> list[Chat]:
        response = self._chatbot_provider.get_chats(status=2, type_chat=1)
        chats = []
        
        if response.status_code == 200:
            for data in response.json().get('chats', []):
                chats.append(get_chat_instance(data))

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
        return chats
    
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