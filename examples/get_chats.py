import os
from dotenv import load_dotenv
from gchat_sdk.controllers import ChatController
from gchat_sdk.providers import ChatBotProvider

load_dotenv()

URL_API = 'URL API'
TOKEN_API = 'TOKEN API'

END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE = True
END_CHATS_WITH_CONTACTS_LAST_MESSAGE = False
TIMEOUT = 0.1
ALERT_TIME = 0.3
ALERT_MESSAGE_TEXT = '''
🔔 Olá! Percebemos que você está inativo há algum tempo.
Para otimizar nosso atendimento, esta conversa será encerrada automaticamente em 5 minutos !
Caso precise de algo, é só nos chamar novamente.

👋 Agradecemos o contato e estamos à disposição!
'''

provider = ChatBotProvider(
    base_url=URL_API,
    access_token=TOKEN_API
)
controller = ChatController(provider, ALERT_MESSAGE_TEXT)
data = controller.get_chats_without_response(
    END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE, 
    END_CHATS_WITH_CONTACTS_LAST_MESSAGE, 
    TIMEOUT
)