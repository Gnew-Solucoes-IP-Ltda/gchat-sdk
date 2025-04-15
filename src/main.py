from controllers import ChatController
from providers.chatbot_provider import ChatBotProvider



provider = ChatBotProvider(
    base_url='https://api.gchat.app.br',
    access_token='663642c06f4ed0c2657819fc'
)
controller = ChatController(provider)
chats = controller.get_chats_without_response(hours=8, is_me=True)
result = controller.finalize_chats(chats)
print(result)
