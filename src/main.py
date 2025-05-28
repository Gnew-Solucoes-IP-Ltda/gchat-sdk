#!/usr/src/gchat/encerrar-chat/venv/bin/python
from controllers import ChatController
from providers.chatbot_provider import ChatBotProvider
from settings import (
    END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE,
    END_CHATS_WITH_CONTACTS_LAST_MESSAGE,
    TIMEOUT,
    TOKEN_API,
    URL_API, 
)


provider = ChatBotProvider(
    base_url=URL_API,
    access_token=TOKEN_API
)
controller = ChatController(provider)
data = controller.finish_chats(
    END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE, 
    END_CHATS_WITH_CONTACTS_LAST_MESSAGE, 
    TIMEOUT
)
print(data)
