import json
from unittest import TestCase
from unittest.mock import MagicMock
from gchat_sdk.controllers.native_channel_controller import NativeChannelController
from gchat_sdk.entities.native_channel import NativeChannelError


BOOTSTRAP_DATA = {
    'contextToken': 'context-token',
    'channelKey': '012bc78b6f522edf',
    'termsVersion': '2026-07-01',
}

GUEST_SESSION_DATA = {
    'token': 'session-token',
    'expiresAt': '2026-10-17T13:52:56.194Z',
    'handle': {
        'handle': 'tatianno_9ye9ox',
        'name': 'Tatianno',
        'certified': False,
        'isGuest': True,
    },
    'remember': False,
    'realtimeContextToken': 'realtime-token',
}

ACTIVE_CONVERSATION = {
    'conversationId': '6ad22c3a3b3c1c0433a488e8',
    'state': 'active',
    'expiresAt': '2026-10-17T13:52:58.712Z',
}

CLOSED_CONVERSATION = {
    'conversationId': '6ad22c3a3b3c1c0433a488e8',
    'state': 'closed',
    'closedAt': '2026-10-16T17:02:15.5267662Z',
    'closedBy': 'visitor',
    'closedSource': 'widget',
}


def make_response(status_code: int = 200, data: dict = None) -> MagicMock:
    content = json.dumps(data).encode() if data is not None else b''
    return MagicMock(
        status_code=status_code,
        ok=200 <= status_code < 300,
        content=content,
        json=MagicMock(return_value=data),
    )


def make_provider() -> MagicMock:
    provider = MagicMock()
    provider.public_bootstrap.return_value = make_response(200, BOOTSTRAP_DATA)
    provider.create_guest_session.return_value = make_response(200, GUEST_SESSION_DATA)
    provider.start_conversation.return_value = make_response(200, ACTIVE_CONVERSATION)
    provider.send_message.return_value = make_response(200, {'messageId': '6ad2562f2e0d591cfb17e801'})
    provider.ack_messages.return_value = make_response(204)
    provider.finalize_conversation.return_value = make_response(200, CLOSED_CONVERSATION)
    provider.delete_session.return_value = make_response(204)
    return provider


def make_controller(provider: MagicMock) -> NativeChannelController:
    return NativeChannelController(provider, 'gnew', device_id='device-1', sleep_func=MagicMock())


def make_logged_controller(provider: MagicMock) -> NativeChannelController:
    controller = make_controller(provider)
    controller.create_guest_session('Tatianno', 'tatianno@gnew.com.br', '+5511997799298')
    return controller


class NativeChannelControllerTestCase(TestCase):

    def test_bootstrap(self):
        provider = make_provider()
        controller = make_controller(provider)
        data = controller.bootstrap()
        provider.public_bootstrap.assert_called_once_with('gnew')
        self.assertEqual(data['contextToken'], 'context-token')

    def test_create_guest_session(self):
        provider = make_provider()
        controller = make_logged_controller(provider)
        context_token, payload = provider.create_guest_session.call_args.args
        self.assertEqual(context_token, 'context-token')
        self.assertEqual(payload['deviceId'], 'device-1')
        self.assertEqual(payload['acceptedTermsVersion'], '2026-07-01')
        self.assertEqual(len(payload['operationId']), 43)
        self.assertEqual(len(payload['visitProof']), 43)
        self.assertEqual(controller.session.token, 'session-token')
        self.assertEqual(controller.session.handle, 'tatianno_9ye9ox')
        self.assertEqual(controller.session.visit_proof, payload['visitProof'])

    def test_create_guest_session_reuses_operation_id_on_retry(self):
        provider = make_provider()
        provider.create_guest_session.side_effect = [
            make_response(500, {'code': 'INTERNAL'}),
            make_response(200, GUEST_SESSION_DATA),
        ]
        controller = make_controller(provider)

        with self.assertRaises(NativeChannelError):
            controller.create_guest_session('Tatianno', 'tatianno@gnew.com.br', '+5511997799298')

        controller.create_guest_session('Tatianno', 'tatianno@gnew.com.br', '+5511997799298')
        first, second = [call.args[1] for call in provider.create_guest_session.call_args_list]
        self.assertEqual(first['operationId'], second['operationId'])

    def test_create_guest_session_new_operation_id_when_payload_changes(self):
        provider = make_provider()
        provider.create_guest_session.side_effect = [
            make_response(500, {'code': 'INTERNAL'}),
            make_response(200, GUEST_SESSION_DATA),
        ]
        controller = make_controller(provider)

        with self.assertRaises(NativeChannelError):
            controller.create_guest_session('Tatianno', 'tatianno@gnew.com.br', '+5511997799298')

        controller.create_guest_session('Tatianno Alves', 'tatianno@gnew.com.br', '+5511997799298')
        first, second = [call.args[1] for call in provider.create_guest_session.call_args_list]
        self.assertNotEqual(first['operationId'], second['operationId'])

    def test_requires_session(self):
        controller = make_controller(make_provider())

        with self.assertRaises(RuntimeError):
            controller.send_message('oi')

    def test_start_conversation(self):
        provider = make_provider()
        controller = make_logged_controller(provider)
        conversation = controller.start_conversation()
        provider.start_conversation.assert_called_once_with('session-token', None)
        self.assertEqual(conversation['state'], 'active')

    def test_start_conversation_after_closed(self):
        provider = make_provider()
        controller = make_logged_controller(provider)
        controller.conversation = CLOSED_CONVERSATION
        controller.start_conversation()
        provider.start_conversation.assert_called_once_with('session-token', '6ad22c3a3b3c1c0433a488e8')

    def test_start_conversation_conflict_adopts_server_state(self):
        provider = make_provider()
        provider.start_conversation.return_value = make_response(
            409, {'code': 'CONVERSATION_CHANGED', 'conversation': ACTIVE_CONVERSATION}
        )
        controller = make_logged_controller(provider)
        conversation = controller.start_conversation()
        self.assertEqual(conversation, ACTIVE_CONVERSATION)

    def test_send_message(self):
        provider = make_provider()
        controller = make_logged_controller(provider)
        message_id = controller.send_message('oi', client_key='client-1')
        provider.send_message.assert_called_once_with('session-token', 'oi', 'client-1')
        self.assertEqual(message_id, '6ad2562f2e0d591cfb17e801')

    def test_get_messages_advances_cursor(self):
        provider = make_provider()
        provider.get_messages.return_value = make_response(200, {
            'messages': [{'id': 'm1', 'direction': 'out', 'text': 'oi'}],
            'cursor': '1792169519_m1',
            'conversation': ACTIVE_CONVERSATION,
        })
        controller = make_logged_controller(provider)
        messages = controller.get_messages()
        provider.get_messages.assert_called_once_with('session-token', None, 100)
        self.assertEqual(len(messages), 1)
        self.assertEqual(controller.cursor, '1792169519_m1')
        self.assertEqual(controller.conversation, ACTIVE_CONVERSATION)

    def test_poll_acks_incoming_and_stops_when_closed(self):
        provider = make_provider()
        provider.get_messages.side_effect = [
            make_response(200, {
                'messages': [
                    {'id': 'm1', 'direction': 'out', 'text': 'oi'},
                    {'id': 'm2', 'direction': 'in', 'text': 'Olá'},
                ],
                'cursor': 'c2',
                'conversation': ACTIVE_CONVERSATION,
            }),
            make_response(200, {'messages': [], 'cursor': 'c2', 'conversation': ACTIVE_CONVERSATION}),
            make_response(200, {'messages': [], 'cursor': 'c2', 'conversation': CLOSED_CONVERSATION}),
        ]
        controller = make_logged_controller(provider)
        batches = list(controller.poll(interval=5))
        self.assertEqual(len(batches), 1)
        self.assertEqual([m['id'] for m in batches[0]], ['m1', 'm2'])
        provider.ack_messages.assert_any_call('session-token', 'delivered', ['m2'])
        provider.ack_messages.assert_any_call('session-token', 'read', ['m2'])
        controller._sleep.assert_called_once_with(5)
        self.assertTrue(controller.is_conversation_ended())

    def test_finalize_conversation(self):
        provider = make_provider()
        controller = make_logged_controller(provider)
        controller.start_conversation()
        conversation = controller.finalize_conversation()
        provider.finalize_conversation.assert_called_once_with('session-token', '6ad22c3a3b3c1c0433a488e8')
        self.assertEqual(conversation['state'], 'closed')

    def test_error_code_parsing(self):
        provider = make_provider()
        provider.send_message.return_value = make_response(
            409, {'title': 'CONVERSATION_START_REQUIRED'}
        )
        controller = make_logged_controller(provider)

        with self.assertRaises(NativeChannelError) as context:
            controller.send_message('oi')

        self.assertEqual(context.exception.status, 409)
        self.assertEqual(context.exception.code, 'CONVERSATION_START_REQUIRED')

    def test_logout_ignores_invalid_session(self):
        provider = make_provider()
        provider.delete_session.return_value = make_response(401, {'code': 'SESSION_INVALID'})
        controller = make_logged_controller(provider)
        controller.logout()
        self.assertIsNone(controller.session)
