"""Request/response types shared by every provider."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..util import canonical_json, sha256_text


class Pending(Exception):
    """The request has been queued for an external operator and has no answer yet."""

    def __init__(self, keys):
        self.keys = list(keys) if isinstance(keys, (list, tuple, set)) else [keys]
        super().__init__(f"{len(self.keys)} request(s) waiting in the queue")


class BudgetExceeded(Exception):
    pass


class ProviderError(Exception):
    pass


@dataclass
class LLMRequest:
    role: str
    system: str
    user: str
    expect_json: bool = True
    schema_hint: str = ""
    tag: str = ""                  # item identity for humans: e.g. "witness:FRD-X"
    max_output_tokens: int | None = None
    temperature: float | None = None
    salt: str = ""                 # forces a distinct, independent request (e.g. pass B)
    meta: dict = field(default_factory=dict)   # not sent; stored with the record

    def key(self, model_identity: str) -> str:
        body = {
            "role": self.role, "system": self.system, "user": self.user,
            "expect_json": self.expect_json, "model": model_identity,
            "temperature": self.temperature, "salt": self.salt,
        }
        return sha256_text(canonical_json(body))[:24]

    def to_record(self) -> dict:
        d = asdict(self)
        return d


@dataclass
class LLMResponse:
    text: str
    parsed: Any = None
    provider: str = ""
    model: str = ""
    usage: dict = field(default_factory=dict)
    cost_usd: float | None = None
    started: str = ""
    finished: str = ""
    key: str = ""
    cached: bool = False
    attempts: int = 1
    parse_error: str = ""

    def to_record(self) -> dict:
        return asdict(self)
