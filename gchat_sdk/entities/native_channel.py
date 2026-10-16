from dataclasses import dataclass, field
from typing import Optional


class NativeChannelError(Exception):

    def __init__(self, status: int, code: str, body: Optional[dict] = None):
        super().__init__(f'{status} {code}')
        self.status = status
        self.code = code
        self.body = body or {}


@dataclass
class GuestSession:
    token: str
    expires_at: str
    handle: str
    name: str
    remember: bool
    visit_proof: str
    realtime_context_token: Optional[str] = None
    raw: dict = field(default_factory=dict)
