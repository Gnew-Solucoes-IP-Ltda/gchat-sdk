import secrets
import time
import uuid
from typing import Callable, Iterator, Optional

import requests

from gchat_sdk.entities.native_channel import GuestSession, NativeChannelError
from gchat_sdk.providers.native_channel_provider import NativeChannelProvider


ENDED_STATES = ('closed', 'expired')


def generate_random_token() -> str:
    # Equivalente ao P1() do widget: 32 bytes aleatórios em base64url sem padding (43 chars)
    return secrets.token_urlsafe(32)


class NativeChannelController:
    """Ciclo de vida de um convidado no canal nativo do Gchat.

    bootstrap -> create_guest_session -> start_conversation -> send_message/poll
    -> finalize_conversation -> logout
    """

    def __init__(
        self,
        provider: NativeChannelProvider,
        handle: str,
        device_id: Optional[str] = None,
        sleep_func: Callable[[float], None] = time.sleep,
    ):
        self._provider = provider
        self._handle = handle
        self._sleep = sleep_func

        # deviceId deve ser persistido pelo chamador e reaproveitado entre sessões
        self.device_id = device_id or str(uuid.uuid4())

        self.bootstrap_data: Optional[dict] = None
        self.session: Optional[GuestSession] = None
        self.conversation: Optional[dict] = None
        self.cursor: Optional[str] = None

        self._operation: Optional[tuple[dict, str]] = None

    def bootstrap(self) -> dict:
        """Obtém contextToken, channelKey e termsVersion do canal."""
        self.bootstrap_data = self._check(self._provider.public_bootstrap(self._handle))
        return self.bootstrap_data

    def create_guest_session(self, name: str, email: str, phone: str, remember: bool = False) -> GuestSession:
        """Cria o convidado e guarda o Bearer token. phone deve estar em E.164 (+5511999999999)."""
        if not self.bootstrap_data:
            self.bootstrap()

        payload = {
            'name': name,
            'email': email,
            'phone': phone,
            'remember': remember,
            'acceptedTermsVersion': self.bootstrap_data.get('termsVersion') or '',
        }

        # operationId é chave de idempotência: reaproveita em retry do mesmo payload
        if not self._operation or self._operation[0] != payload:
            self._operation = (payload, generate_random_token())

        visit_proof = self.session.visit_proof if self.session else generate_random_token()
        data = self._check(
            self._provider.create_guest_session(
                self.bootstrap_data['contextToken'],
                {
                    **payload,
                    'deviceId': self.device_id,
                    'operationId': self._operation[1],
                    'visitProof': visit_proof,
                },
            )
        )
        self._operation = None
        handle = data.get('handle') or {}
        self.session = GuestSession(
            token=data['token'],
            expires_at=data.get('expiresAt', ''),
            handle=handle.get('handle', ''),
            name=handle.get('name', name),
            remember=data.get('remember', remember),
            visit_proof=visit_proof,
            realtime_context_token=data.get('realtimeContextToken'),
            raw=data,
        )
        self._update_conversation(data.get('conversation'))
        self.cursor = None
        return self.session

    def start_conversation(self) -> dict:
        """Abre a conversa, ou reabre uma encerrada/expirada."""
        expected_closed_id = None

        if self.is_conversation_ended():
            expected_closed_id = self.conversation.get('conversationId')

        try:
            conversation = self._check(
                self._provider.start_conversation(self._token(), expected_closed_id)
            )

        except NativeChannelError as error:
            # 409: a conversa mudou no servidor; o corpo pode trazer o estado atual
            if error.status == 409 and isinstance(error.body.get('conversation'), dict):
                self._update_conversation(error.body['conversation'])
                return self.conversation

            raise

        self._update_conversation(conversation)
        return self.conversation

    def send_message(self, text: str, client_key: Optional[str] = None) -> str:
        """Envia texto e devolve o messageId."""
        data = self._check(
            self._provider.send_message(self._token(), text, client_key or str(uuid.uuid4()))
        )
        return data['messageId']

    def get_messages(self, after: Optional[str] = None, limit: int = 100) -> list[dict]:
        """Busca uma página de mensagens a partir do cursor e o avança."""
        data = self._check(
            self._provider.get_messages(self._token(), after if after is not None else self.cursor, limit)
        )

        if data.get('cursor'):
            self.cursor = data['cursor']

        self._update_conversation(data.get('conversation'))
        return data.get('messages', [])

    def fetch_new_messages(self) -> list[dict]:
        """Pagina até não haver mais mensagens novas."""
        messages = []

        while True:
            previous = self.cursor
            page = self.get_messages()
            messages.extend(page)

            if not page or self.cursor == previous:
                return messages

    def ack(self, message_ids: list[str], kind: str = 'read') -> None:
        """Confirma mensagens recebidas. kind: 'delivered' ou 'read'."""
        if message_ids:
            self._check(self._provider.ack_messages(self._token(), kind, message_ids))

    def poll(self, interval: float = 10, ack: bool = True) -> Iterator[list[dict]]:
        """Gera lotes de mensagens novas até a conversa ser encerrada ou expirar."""
        while True:
            messages = self.fetch_new_messages()

            if messages:
                incoming = [message['id'] for message in messages if message.get('direction') == 'in']

                if ack and incoming:
                    self.ack(incoming, 'delivered')
                    self.ack(incoming, 'read')

                yield messages

            if self.is_conversation_ended():
                return

            self._sleep(interval)

    def is_conversation_ended(self) -> bool:
        return bool(self.conversation) and self.conversation.get('state') in ENDED_STATES

    def finalize_conversation(self) -> dict:
        """Encerra a conversa atual."""
        if not self.conversation or not self.conversation.get('conversationId'):
            raise RuntimeError('Nenhuma conversa para finalizar.')

        conversation = self._check(
            self._provider.finalize_conversation(self._token(), self.conversation['conversationId'])
        )
        self._update_conversation(conversation)
        return self.conversation

    def logout(self) -> None:
        """Revoga o token do convidado."""
        if not self.session:
            return

        try:
            self._check(self._provider.delete_session(self.session.token))

        except NativeChannelError as error:
            if error.code not in ('SESSION_INVALID', 'SESSION_REVOKED'):
                raise

        self.session = None
        self.conversation = None
        self.cursor = None

    def _token(self) -> str:
        if not self.session:
            raise RuntimeError('Sessão não iniciada: chame create_guest_session() antes.')

        return self.session.token

    def _update_conversation(self, conversation: Optional[dict]) -> None:
        if conversation is not None:
            self.conversation = conversation

    @staticmethod
    def _check(response: requests.Response) -> dict:
        if not response.ok:
            raise NativeChannelController._parse_error(response)

        if response.status_code == 204 or not response.content:
            return {}

        return response.json()

    @staticmethod
    def _parse_error(response: requests.Response) -> NativeChannelError:
        try:
            body = response.json()

        except ValueError:
            body = {}

        if not isinstance(body, dict):
            body = {}

        code = f'HTTP_{response.status_code}'

        for key in ('code', 'errorCode', 'reason', 'title'):
            value = body.get(key)

            if isinstance(value, str) and value.strip():
                code = value.strip()
                break

        return NativeChannelError(response.status_code, code, body)
