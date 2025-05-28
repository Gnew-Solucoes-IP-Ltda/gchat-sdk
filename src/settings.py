import os
from dotenv import load_dotenv


load_dotenv()


URL_API = os.environ.get('URL_API')
TOKEN_API = os.environ.get('TOKEN_API')


END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE = bool(os.environ.get('END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE') == 'True')
END_CHATS_WITH_CONTACTS_LAST_MESSAGE = bool(os.environ.get('END_CHATS_WITH_CONTACTS_LAST_MESSAGE') == 'True')
TIMEOUT = int(os.environ.get('TIMEOUT'))