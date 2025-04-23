#!/usr/src/gchat/encerrar-chat/venv/bin/python
from controllers import ChatController
from providers.chatbot_provider import ChatBotProvider



provider = ChatBotProvider(
    base_url='https://api.gchat.app.br',
    access_token='67d84c27610880ae17cc3fb8'
)

request_executed = False
chats = []
controller = ChatController(provider)

while len(chats) != 0 or request_executed == False:
    chats = controller.get_chats_without_response(hours=24, is_me=True)
    chats.extend(controller.get_chats_without_response(hours=24, is_me=False))
    result = controller.finalize_chats(chats)
    print(result)

    if len(chats) == 0:
        request_executed = True
