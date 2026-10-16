from typing import Optional

import requests


class NativeChannelProvider:
    """Cliente HTTP do canal nativo (widget/sala pública) do Gchat.

    Cada método faz uma única chamada e devolve o requests.Response cru;
    o tratamento de estado e de erros fica no NativeChannelController.
    """

    def __init__(self, base_url: str, timeout: float = 15, session: Optional[requests.Session] = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._http = session or requests.Session()

    def public_bootstrap(self, handle: str) -> requests.Response:
        return self._request('POST', '/v1/widget/public/bootstrap', json={'handle': handle})

    def create_guest_session(self, context_token: str, data: dict) -> requests.Response:
        return self._request(
            'POST',
            '/v1/widget/session/guest',
            json=data,
            headers={'X-Widget-Context': context_token},
        )

    def start_conversation(self, token: str, expected_closed_conversation_id: Optional[str] = None) -> requests.Response:
        data = {}

        if expected_closed_conversation_id:
            data['expectedClosedConversationId'] = expected_closed_conversation_id

        return self._request('POST', '/v1/widget/conversation/start', json=data, token=token)

    def send_message(self, token: str, text: str, client_key: str) -> requests.Response:
        return self._request(
            'POST',
            '/v1/widget/messages',
            json={'text': text, 'clientKey': client_key},
            token=token,
        )

    def get_messages(self, token: str, after: Optional[str] = None, limit: int = 100) -> requests.Response:
        params = {'limit': str(limit)}

        if after:
            params['after'] = after

        return self._request('GET', '/v1/widget/messages', params=params, token=token)

    def ack_messages(self, token: str, kind: str, message_ids: list[str]) -> requests.Response:
        return self._request(
            'POST',
            '/v1/widget/messages/ack',
            json={'type': kind, 'messageIds': message_ids},
            token=token,
        )

    def finalize_conversation(self, token: str, conversation_id: str) -> requests.Response:
        return self._request(
            'POST',
            '/v1/widget/conversation/finalize',
            json={'expectedConversationId': conversation_id},
            token=token,
        )

    def delete_session(self, token: str) -> requests.Response:
        return self._request('DELETE', '/v1/widget/session', token=token)

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        token: Optional[str] = None,
    ) -> requests.Response:
        all_headers = {'Accept': 'application/json', **(headers or {})}

        if token:
            all_headers['Authorization'] = f'Bearer {token}'

        return self._http.request(
            method,
            f'{self.base_url}{path}',
            json=json,
            params=params,
            headers=all_headers,
            timeout=self.timeout,
        )
