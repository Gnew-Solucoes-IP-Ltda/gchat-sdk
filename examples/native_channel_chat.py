import os
from dotenv import load_dotenv
from gchat_sdk.controllers import NativeChannelController
from gchat_sdk.providers import NativeChannelProvider

load_dotenv()

NATIVE_URL = os.environ.get('NATIVE_URL', 'https://access.gchat.app.br')
NATIVE_HANDLE = os.environ.get('NATIVE_HANDLE')

provider = NativeChannelProvider(base_url=NATIVE_URL)
controller = NativeChannelController(provider, NATIVE_HANDLE)

controller.bootstrap()
controller.create_guest_session(
    name='Fulano de Tal',
    email='fulano@exemplo.com.br',
    phone='+5511999999999'
)
controller.start_conversation()
controller.send_message('Olá')

try:
    for messages in controller.poll(interval=10):
        for message in messages:
            if message.get('direction') == 'in':
                print('<', message.get('text'))

except KeyboardInterrupt:
    controller.finalize_conversation()

finally:
    controller.logout()
