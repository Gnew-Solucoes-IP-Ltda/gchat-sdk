# GCHAT Close Conversations

This project automates sending alerts and closing inactive conversations on the GCHAT platform, using API integration.

## Repository

https://github.com/Gnew-Solucoes-IP-Ltda/gchat-sdk

## Features

- Automatically sends alert messages to inactive contacts.
- Automatically closes conversations based on configurable criteria.
- Flexible configuration via environment variables.

## Project Structure

```
.
├── gchat_sdk/
│   ├── controllers/
│   ├── entities/
│   ├── factories/
│   ├── providers/
│   ├── tests/
│   ├── main.py
│   ├── settings.py
│   └── utils.py
├── examples/
│   └── finish_chats.py
├── .env
├── requirements.txt
└── LICENSE
```

## Installation

1. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```sh
   pip install gchat-sdk
   ```

4. Configure environment variables in the `.env` file:
   ```
   URL_API=https://api.gchat.app.br
   TOKEN_API=your_token
   END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE=True
   END_CHATS_WITH_CONTACTS_LAST_MESSAGE=True
   TIMEOUT=1
   ALERT_TIME=0.1
   ```

## Usage

Run the example to send alerts and close inactive conversations:

```python
import os
from dotenv import load_dotenv
from gchat_sdk.controllers.chat_controller import ChatController
from gchat_sdk.providers.chatbot_provider import ChatBotProvider


load_dotenv()


URL_API = os.environ.get('URL_API')
TOKEN_API = os.environ.get('TOKEN_API')

END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE = True
END_CHATS_WITH_CONTACTS_LAST_MESSAGE = True
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
    END_CHATS_WITH_ATTENDANTS_LAST_MESSAGE, 
    END_CHATS_WITH_CONTACTS_LAST_MESSAGE, 
    TIMEOUT
)
print('closed chats', data)
```

## Native channel (guest chat)

`NativeChannelController` talks to the Gchat native channel (the public web chat at `https://access.gchat.app.br/room/<handle>`) as a guest visitor. It covers the whole lifecycle: bootstrap, guest session, conversation start, sending messages, polling and finishing.

```python
from gchat_sdk.controllers import NativeChannelController
from gchat_sdk.providers import NativeChannelProvider

provider = NativeChannelProvider(base_url='https://access.gchat.app.br')
controller = NativeChannelController(provider, handle='your_channel_handle')

controller.bootstrap()
controller.create_guest_session('Name', 'name@example.com', '+5511999999999')  # phone in E.164
controller.start_conversation()
controller.send_message('Hello')

for messages in controller.poll(interval=10):  # stops when the conversation is closed/expired
    for message in messages:
        print(message['direction'], message.get('text'))

controller.finalize_conversation()
controller.logout()
```

- `device_id` identifies the device; persist `controller.device_id` and pass it back to the constructor to reuse it across runs.
- Non-2xx responses raise `NativeChannelError` with `status`, `code` (e.g. `RATE_LIMIT_EXCEEDED`, `CONVERSATION_START_REQUIRED`, `SESSION_INVALID`) and `body`.
- `poll()` acknowledges incoming messages as `delivered` and `read`; pass `ack=False` and call `controller.ack(ids, 'read')` yourself to control read receipts.

See `examples/native_channel_chat.py`.

## Testing

Unit tests are located in `gchat_sdk/tests/`. To run the tests using `unittest`:

```sh
python -m unittest discover gchat_sdk/tests/
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
