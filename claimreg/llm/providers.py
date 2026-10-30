"""Model providers.

* ``openai``    - any OpenAI-compatible Chat Completions endpoint (OpenAI,
                  DeepSeek, OpenRouter, Together, a local server ...).
* ``anthropic`` - Anthropic Messages API.
* ``queue``     - file queue: the request is written to disk and an external
                  operator (a person with NotebookLM or a chat window, or an
                  agent) writes the answer back.  The harness resumes when the
                  answer exists.
* ``replay``    - answers only from the cache; never contacts anything.
* ``mock``      - deterministic offline answers for tests.

API keys are read from an environment variable or a key file at call time,
held only in memory, and never written to any log, cache or artifact.
"""

from __future__ import annotations

import http.client
import json
import os
import random
import time
import urllib.error
import urllib.request
from pathlib import Path

from ..util import ensure_dir, read_json, read_text, utcnow, write_json
from .base import LLMRequest, LLMResponse, Pending, ProviderError


def _api_key(pcfg: dict) -> str:
    env = pcfg.get("api_key_env")
    if env and os.environ.get(env):
        return os.environ[env].strip()
    kf = pcfg.get("api_key_file")
    if kf:
        p = Path(os.path.expanduser(kf))
        if p.exists():
            return read_text(p).strip()
        raise ProviderError(f"api_key_file not found: {kf}")
    raise ProviderError(
        f"No API key: set environment variable {env!r} or 'api_key_file' in the "
        f"provider config. Keys are never stored by the harness.")


def _post_json(url: str, body: dict, headers: dict, timeout: float) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", errors="replace")[:2000]
        except Exception:
            detail = ""
        err = ProviderError(f"HTTP {e.code} from {url}: {detail}")
        err.status = e.code  # type: ignore[attr-defined]
        raise err
    except urllib.error.URLError as e:
        err = ProviderError(f"network error contacting {url}: {e.reason}")
        err.status = 0  # type: ignore[attr-defined]
        raise err
    except (http.client.HTTPException, ConnectionError, TimeoutError, OSError, ValueError) as e:
        # dropped connections, read timeouts and truncated bodies are transient: retried by the router
        err = ProviderError(f"connection problem with {url}: {type(e).__name__}: {e}")
        err.status = 0  # type: ignore[attr-defined]
        raise err


class BaseProvider:
    kind = "base"

    def __init__(self, name: str, pcfg: dict, project_dir: Path):
        self.name = name
        self.cfg = pcfg
        self.project_dir = Path(project_dir)

    @property
    def model(self) -> str:
        return str(self.cfg.get("model", "unknown"))

    @property
    def identity(self) -> str:
        return f"{self.kind}:{self.model}"

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:  # pragma: no cover
        raise NotImplementedError

    def cost(self, usage: dict) -> float | None:
        pin = self.cfg.get("price_per_mtok_in")
        pout = self.cfg.get("price_per_mtok_out")
        if pin is None or pout is None or not usage:
            return None
        return (usage.get("input_tokens", 0) * float(pin)
                + usage.get("output_tokens", 0) * float(pout)) / 1e6


class OpenAICompatible(BaseProvider):
    kind = "openai"

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:
        base = self.cfg.get("base_url", "https://api.openai.com/v1").rstrip("/")
        url = base + "/chat/completions"
        body: dict = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": req.system},
                {"role": "user", "content": req.user},
            ],
        }
        mot = req.max_output_tokens or self.cfg.get("max_output_tokens")
        if mot:
            param = self.cfg.get("max_tokens_param") or (
                "max_completion_tokens" if "api.openai.com" in base else "max_tokens")
            body[param] = int(mot)
        temp = req.temperature if req.temperature is not None else self.cfg.get("temperature")
        if temp is not None:
            body["temperature"] = float(temp)
        if req.expect_json and self.cfg.get("json_mode"):
            body["response_format"] = {"type": "json_object"}
        for k, v in (self.cfg.get("extra_body") or {}).items():
            body[k] = v
        headers = {"Authorization": f"Bearer {_api_key(self.cfg)}"}
        for k, v in (self.cfg.get("extra_headers") or {}).items():
            headers[k] = v
        started = utcnow()
        data = _post_json(url, body, headers, float(self.cfg.get("timeout_s", 900)))
        try:
            msg = data["choices"][0]["message"]
            text = msg.get("content") or ""
            if isinstance(text, list):
                text = "".join(p.get("text", "") for p in text if isinstance(p, dict))
        except Exception as e:
            raise ProviderError(f"unexpected response shape: {str(data)[:500]}") from e
        u = data.get("usage") or {}
        usage = {"input_tokens": u.get("prompt_tokens", 0),
                 "output_tokens": u.get("completion_tokens", 0)}
        return LLMResponse(text=text, provider=self.name, model=data.get("model", self.model),
                           usage=usage, cost_usd=self.cost(usage), started=started,
                           finished=utcnow(), key=key)


class Anthropic(BaseProvider):
    kind = "anthropic"

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:
        base = self.cfg.get("base_url", "https://api.anthropic.com/v1").rstrip("/")
        url = base + "/messages"
        body: dict = {
            "model": self.model,
            "max_tokens": int(req.max_output_tokens or self.cfg.get("max_output_tokens", 8000)),
            "system": req.system,
            "messages": [{"role": "user", "content": req.user}],
        }
        temp = req.temperature if req.temperature is not None else self.cfg.get("temperature")
        if temp is not None:
            body["temperature"] = float(temp)
        headers = {"x-api-key": _api_key(self.cfg),
                   "anthropic-version": self.cfg.get("api_version", "2023-06-01")}
        started = utcnow()
        data = _post_json(url, body, headers, float(self.cfg.get("timeout_s", 900)))
        try:
            text = "".join(b.get("text", "") for b in data.get("content", [])
                           if b.get("type") == "text")
        except Exception as e:
            raise ProviderError(f"unexpected response shape: {str(data)[:500]}") from e
        u = data.get("usage") or {}
        usage = {"input_tokens": u.get("input_tokens", 0),
                 "output_tokens": u.get("output_tokens", 0)}
        return LLMResponse(text=text, provider=self.name, model=data.get("model", self.model),
                           usage=usage, cost_usd=self.cost(usage), started=started,
                           finished=utcnow(), key=key)


class QueueProvider(BaseProvider):
    """File-queue provider: pending/<key>.json  ->  done/<key>.txt"""

    kind = "queue"

    @property
    def qdir(self) -> Path:
        d = Path(self.cfg.get("dir", "queue"))
        if not d.is_absolute():
            d = self.project_dir / d
        return d

    def done_text(self, key: str) -> str | None:
        for ext in (".txt", ".md", ".json"):
            p = self.qdir / "done" / f"{key}{ext}"
            if p.exists():
                raw = read_text(p)
                if ext == ".json":
                    try:
                        obj = json.loads(raw)
                        if isinstance(obj, dict) and "text" in obj and len(obj) <= 3:
                            return obj["text"]
                    except Exception:
                        pass
                return raw
        return None

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:
        skip = read_json(self.qdir / "done" / f"{key}.skip.json", default=None)
        if skip is not None:
            raise ProviderError(f"request skipped by the queue operator ({skip.get('operator', '?')}): "
                                f"{skip.get('reason', 'no reason given')}")
        text = self.done_text(key)
        if text is None:
            pend = self.qdir / "pending" / f"{key}.json"
            if not pend.exists():
                write_json(pend, {
                    "key": key, "role": req.role, "tag": req.tag,
                    "expect_json": req.expect_json, "schema_hint": req.schema_hint,
                    "system": req.system, "user": req.user, "created": utcnow(),
                    "salt": req.salt,
                })
            raise Pending(key)
        pend = self.qdir / "pending" / f"{key}.json"
        if pend.exists():
            ensure_dir(self.qdir / "answered")
            try:
                os.replace(pend, self.qdir / "answered" / f"{key}.json")
            except OSError:
                pass
        meta = read_json(self.qdir / "done" / f"{key}.meta.json", default={}) or {}
        model = meta.get("model") or self.cfg.get("model", "queue-operator")
        return LLMResponse(text=text, provider=self.name, model=model,
                           usage={}, cost_usd=None, started=meta.get("started", ""),
                           finished=meta.get("finished", utcnow()), key=key)


class ReplayProvider(BaseProvider):
    kind = "replay"

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:
        raise ProviderError(f"replay provider: no cached answer for request {key} "
                            f"({req.role} {req.tag})")


def make_provider(name: str, pcfg: dict, project_dir: Path) -> BaseProvider:
    t = pcfg.get("type", name)
    if t == "openai":
        return OpenAICompatible(name, pcfg, project_dir)
    if t == "anthropic":
        return Anthropic(name, pcfg, project_dir)
    if t == "queue":
        return QueueProvider(name, pcfg, project_dir)
    if t == "replay":
        return ReplayProvider(name, pcfg, project_dir)
    if t == "local":
        from .local import LocalProvider
        return LocalProvider(name, pcfg, project_dir)
    if t == "mock":
        from .mock import MockProvider
        return MockProvider(name, pcfg, project_dir)
    raise ProviderError(f"unknown provider type {t!r} for provider {name!r}")


def backoff_sleep(attempt: int) -> None:
    time.sleep(min(60.0, (2 ** attempt) + random.random()))
