"""A scripted stand-in for a model API, for tests that need API behaviour without a network.

``kind`` is "openai", so the router treats it exactly like a live API provider: retries, JSON
repair, failover, budget and concurrency all apply.  A provider entry looks like
``{"type": "scripted", "model": "m1", "script": "name"}`` and ``SCRIPTS[name]`` is a function
``(req, provider) -> str | dict | LLMResponse`` that may raise ProviderError.
"""

import json

from claimreg.llm import providers
from claimreg.llm.base import LLMResponse, ProviderError
from claimreg.util import utcnow

SCRIPTS: dict = {}
CALLS: list = []


def http_error(status: int, body: str = "") -> ProviderError:
    e = ProviderError(f"HTTP {status} from scripted: {body}")
    e.status = status
    return e


class Scripted(providers.BaseProvider):
    kind = "openai"

    def complete(self, req, key):
        CALLS.append((self.name, req.role, req.tag))
        out = SCRIPTS[self.cfg.get("script", self.name)](req, self)
        if isinstance(out, LLMResponse):
            out.provider, out.key = self.name, key
            out.model = out.model or self.model
            return out
        text = out if isinstance(out, str) else json.dumps(out, ensure_ascii=False)
        return LLMResponse(text=text, provider=self.name, model=self.model,
                           usage={"input_tokens": 10, "output_tokens": 10}, cost_usd=0.001,
                           started=utcnow(), finished=utcnow(), key=key, finish_reason="stop")


providers.EXTRA_TYPES["scripted"] = Scripted


def reset():
    SCRIPTS.clear()
    CALLS.clear()
