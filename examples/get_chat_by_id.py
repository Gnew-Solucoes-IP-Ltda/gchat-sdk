import os
from dotenv import load_dotenv
from gchat_sdk.providers import ChatBotProvider

load_dotenv()

URL_API = os.environ.get('URL_API')
TOKEN_API = os.environ.get('TOKEN_API')


provider = ChatBotProvider(
    base_url=URL_API,
    access_token=TOKEN_API
)
# response = provider.get_chats(status=2, type_chat=2)
response = provider.get_chat_by_id('68d66d28c648e6db959cbd09')
print(response.text)