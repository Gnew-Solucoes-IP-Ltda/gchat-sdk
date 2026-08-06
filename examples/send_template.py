import os
from dotenv import load_dotenv
from gchat_sdk.providers import ChatBotProvider

load_dotenv()

URL_API = os.environ.get('URL_API')
TOKEN_API = os.environ.get('TOKEN_API')
TEMPLATE_ID = "6878dace67716e87a462f92b"
TELEFONE_TESTE='1199XXXXX'


provider = ChatBotProvider(
    base_url=URL_API,
    access_token=TOKEN_API
)
response = provider.send_template(
    TELEFONE_TESTE,
    TEMPLATE_ID
)
print(response.status_code)
print(response.text)