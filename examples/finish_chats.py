import os
from dotenv import load_dotenv
from gchat_sdk.controllers import ChatController
from gchat_sdk.providers import ChatBotProvider

load_dotenv()

URL_API = os.environ.get('URL_API')
TOKEN_API = os.environ.get('TOKEN_API')
TIMEOUT = 2
ALERT_TIME = 0.1
ALERT_MESSAGE_TEXT = '''
🔔 Olá! Percebemos que você está inativo há algum tempo.
Para otimizar nosso atendimento, esta conversa será encerrada.
Caso precise de algo, é só nos chamar novamente.

👋 Agradecemos o contato e estamos à disposição!
'''

provider = ChatBotProvider(
    base_url=URL_API,
    access_token=TOKEN_API
)
controller = ChatController(provider, ALERT_MESSAGE_TEXT)
data = controller.alert_chats(alert_time_in_hour=ALERT_TIME)
print('send message alert', data)
data = controller.finish_chats(
    end_attendants_last_message=True,
    end_contacts_last_message=False,
    timeout=TIMEOUT,
    discard_not_alert_message=True
)
print('closed chats', data)
