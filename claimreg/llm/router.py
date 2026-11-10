"""Role routing, caching, budget, logging and JSON handling for model calls.

Usage::

    llm = LLM(cfg, run_dir=...)
    responses = llm.call_many([LLMRequest(...), ...])   # may raise Pending

Every completed call is cached under ``<project>/cache/llm/`` by a key built
from (role, prompts, model identity, temperature, salt).  A rerun with the
same inputs is therefore free and exactly reproducible, and a fork that
changes nothing upstream reuses the parent's answers.

Every call (cached or not) is appended to the run's call log, which is the
reproducibility record required by specification module 20.1.
"""

from __future__ import annotations

import re
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

from ..util import append_jsonl, ensure_dir, read_json, sha256_text, utcnow, write_json
from .base import BudgetExceeded, LLMRequest, LLMResponse, Pending, ProviderError
from .jsonparse import JSONExtractError, extract_json
from .providers import BaseProvider, backoff_sleep, make_provider

JSON_REPAIR = ("Your previous reply could not be parsed as JSON. Reply again with ONLY "
               "the JSON value requested, no prose and no code fence.")


class LLM:
    def __init__(self, cfg: dict, run_dir: str | Path | None = None,
                 log_name: str = "llm-calls.jsonl"):
        self.cfg = cfg
        self.project_dir = Path(cfg["_project_dir"])
        self.run_dir = Path(run_dir) if run_dir else None
        self.cache_dir = ensure_dir(self.project_dir / "cache" / "llm")
        self._providers: dict[str, BaseProvider] = {}
        self._lock = threading.Lock()
        self.log_path = (self.run_dir / "00_RUN-CONTROL" / "model-and-human-decisions" / log_name
                         if self.run_dir else self.project_dir / "cache" / log_name)
        self.state_path = (self.run_dir / "00_RUN-CONTROL" / "budget-state.json"
                           if self.run_dir else self.project_dir / "cache" / "budget-state.json")
        st = read_json(self.state_path, default={}) or {}
        self.error_count = 0          # failed calls in this process (deliberate skips excluded)
        self.failovers = 0            # answers that came from a provider other than the first in its list
        self.down: dict[str, str] = {}   # providers that cannot work in this run (no credits, bad key, no such model)
        self.calls_made = int(st.get("calls_made", 0))
        self.usd_spent = float(st.get("usd_spent", 0.0))

    # ------------------------------------------------------------------ #
    # Routing.  A role is routed to one provider ("openai") or to an ordered list of providers
    # (["deepseek", "openai", "gemini"]).  With a list, a provider that refuses, filters, errors,
    # times out or returns unusable output is skipped and the next one is asked: one provider's
    # refusal or outage can no longer stop a run.  Every skip is recorded with its reason.
    def chain_for(self, role: str) -> list[str]:
        v = self.cfg["roles"].get(role) or self.cfg.get("default_provider") or "openai"
        names = [v] if isinstance(v, str) else [str(x) for x in v if x]
        return names or [self.cfg.get("default_provider") or "openai"]

    def _provider(self, name: str, role: str = "") -> BaseProvider:
        if name not in self._providers:
            pcfg = self.cfg["providers"].get(name)
            if pcfg is None:
                raise ProviderError(f"role {role!r} routed to unknown provider {name!r}")
            self._providers[name] = make_provider(name, pcfg, self.project_dir)
        return self._providers[name]

    def provider_for(self, role: str) -> BaseProvider:
        """The first (preferred) provider for a role."""
        return self._provider(self.chain_for(role)[0], role)

    def providers_for(self, role: str) -> list[BaseProvider]:
        return [self._provider(n, role) for n in self.chain_for(role)]

    def is_model_role(self, role: str) -> bool:
        """True when the role's preferred provider is a real model (API or file queue), not the
        deterministic local engine or the test mock."""
        return self.provider_for(role).kind in ("openai", "anthropic", "queue")

    def is_api_role(self, role: str) -> bool:
        """True when the role's preferred provider is a model API (answers arrive in the same call)."""
        return self.provider_for(role).kind in ("openai", "anthropic")

    def key_for(self, req: LLMRequest) -> str:
        return req.key(self.provider_for(req.role).identity)

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / key[:2] / f"{key}.json"

    def cached(self, req: LLMRequest) -> LLMResponse | None:
        """The stored answer for this exact request.  Every provider in the role's failover list is
        checked, in order.  With ``cache_fallback_providers`` set (e.g. ["queue"]), an answer stored
        under one of those providers is also reused when the role has since been routed elsewhere:
        a run can switch provider and ask only what is still missing.  The reused answer keeps its
        original provider and model in the record."""
        rec = None
        for prov in self.providers_for(req.role):
            rec = read_json(self._cache_path(req.key(prov.identity)))
            if rec:
                break
        if not rec:
            for name in self.cfg.get("cache_fallback_providers", []) or []:
                pcfg = self.cfg["providers"].get(name)
                if not pcfg:
                    continue
                alt = self._provider(name).identity
                rec = read_json(self._cache_path(req.key(alt)))
                if rec:
                    break
        if not rec:
            return None
        r = rec["response"]
        resp = LLMResponse(**{k: v for k, v in r.items() if k in LLMResponse.__dataclass_fields__})
        resp.cached = True
        return resp

    def _save_state(self) -> None:
        write_json(self.state_path, {"calls_made": self.calls_made,
                                     "usd_spent": round(self.usd_spent, 6),
                                     "updated": utcnow()})

    def _log(self, req: LLMRequest, resp: LLMResponse | None, status: str, err: str = "",
             prov: BaseProvider | None = None) -> None:
        prov = prov or self.provider_for(req.role)
        row = {
            "time": utcnow(), "status": status, "role": req.role, "tag": req.tag,
            "key": resp.key if resp else req.key(prov.identity),
            "provider": resp.provider if resp else prov.name,
            "model": resp.model if resp else prov.model,
            "cached": bool(resp and resp.cached),
            "system_sha256": sha256_text(req.system)[:16],
            "user_sha256": sha256_text(req.user)[:16],
            "response_sha256": sha256_text(resp.text)[:16] if resp else "",
            "usage": resp.usage if resp else {}, "cost_usd": resp.cost_usd if resp else None,
            "error": err[:500],
        }
        if resp is not None and resp.failover:
            row["failover"] = resp.failover
        with self._lock:
            append_jsonl(self.log_path, row)

    def _check_budget(self) -> None:
        b = self.cfg.get("budget", {})
        if self.calls_made >= int(b.get("max_calls", 10 ** 9)):
            raise BudgetExceeded(f"call budget reached ({self.calls_made} calls). Raise "
                                 f"budget.max_calls in project.json to continue.")
        if self.usd_spent >= float(b.get("max_usd", 10 ** 9)):
            raise BudgetExceeded(f"cost budget reached (${self.usd_spent:.2f}). Raise "
                                 f"budget.max_usd in project.json to continue.")

    # ------------------------------------------------------------------ #
    LIVE = ("openai", "anthropic")
    REFUSAL_FINISH = ("content_filter", "refusal", "safety", "recitation", "blocked", "prohibited_content")
    _FILTER_BODY = re.compile(r"content[_ ]?filter|content[_ ]?policy|safety|policy|blocked|moderation", re.I)

    @classmethod
    def _error_reason(cls, e: Exception) -> str:
        """A short mechanical label for why a provider was skipped.  Decided from the HTTP status
        and error body only, never from the prose of an answer."""
        status = getattr(e, "status", None)
        msg = str(e)
        if status == 0:
            return "network error or timeout"
        if status in (400, 403, 422) and cls._FILTER_BODY.search(msg):
            return f"HTTP {status}: request blocked by the provider's content filter"
        if status in (401, 403):
            return f"HTTP {status}: key rejected or not permitted"
        if status == 404:
            return "HTTP 404: model or endpoint not found"
        if status == 429:
            return "HTTP 429: rate limit or quota"
        if status:
            return f"HTTP {status}"
        return msg[:160]

    _QUOTA = re.compile(r"insufficient_quota|no credits|credit balance|billing|exceeded your current quota|"
                        r"payment required|account (?:is )?(?:not active|deactivated|suspended)", re.I)

    @classmethod
    def _down_reason(cls, e: Exception) -> str:
        """Non-empty when the error means this provider cannot answer ANY request in this run:
        the key is rejected, the account has no credits, or the model name does not exist.  Such a
        provider is asked once and then skipped, instead of being retried on every call."""
        status = getattr(e, "status", None)
        msg = str(e)
        if status in (402,) or (status in (429, 403, 400) and cls._QUOTA.search(msg)):
            return "the account has no credits or its quota is used up"
        if status == 401:
            return "the API key was rejected"
        if status == 404:
            return "the model name or endpoint was not found"
        return ""

    def _unusable(self, req: LLMRequest, resp: LLMResponse) -> str:
        """Why an answer cannot be used, or "".  Mechanical signals only."""
        fr = (resp.finish_reason or "").lower()
        if fr in self.REFUSAL_FINISH:
            return f"provider stopped the answer ({fr})"
        if not (resp.text or "").strip():
            return "empty answer"
        if req.expect_json and resp.parsed is None:
            return "answer was not valid JSON after one repair attempt"
        if resp.parse_error.startswith("validation:"):
            return resp.parse_error[:160]
        return ""

    def _ask(self, prov: BaseProvider, req: LLMRequest, key: str, validate: Callable | None) -> LLMResponse:
        """One provider: transient-error retries, one JSON repair, validation.  Raises ProviderError
        when the provider cannot be reached or rejects the request."""
        is_live = prov.kind in self.LIVE
        if is_live:
            with self._lock:
                self._check_budget()
        retries = int(self.cfg.get("budget", {}).get("retries", 2))
        attempt = 0
        while True:
            attempt += 1
            try:
                resp = prov.complete(req, key)
                break
            except ProviderError as e:
                status = getattr(e, "status", None)
                transient = status in (0, 408, 409, 425, 429, 500, 502, 503, 504, 529) and not self._down_reason(e)
                if transient and attempt <= retries:
                    backoff_sleep(attempt)
                    continue
                raise
        resp.attempts = attempt
        # A reasoning model can spend its whole output budget thinking and return no text
        # (finish "length").  Ask once more with a larger budget before giving up on it.
        if is_live and not (resp.text or "").strip() and (resp.finish_reason or "").lower() in ("length", "max_tokens"):
            import dataclasses
            cur = int(req.max_output_tokens or prov.cfg.get("max_output_tokens") or 8000)
            bigger = dataclasses.replace(req, max_output_tokens=min(max(cur * 4, 32000), 64000))
            try:
                r2 = prov.complete(bigger, key)
                r2.attempts = attempt + 1
                r2.cost_usd = (r2.cost_usd or 0) + (resp.cost_usd or 0) or None
                if (r2.text or "").strip():
                    resp = r2
            except ProviderError:
                pass
        if req.expect_json:
            try:
                resp.parsed = extract_json(resp.text)
            except JSONExtractError as e:
                resp.parse_error = str(e)
                if is_live and (resp.text or "").strip():
                    fix = LLMRequest(role=req.role, system=req.system,
                                     user=req.user + "\n\n" + JSON_REPAIR,
                                     expect_json=True, tag=req.tag + ":json-repair",
                                     max_output_tokens=req.max_output_tokens,
                                     temperature=req.temperature, salt=req.salt, meta=req.meta)
                    try:
                        r2 = prov.complete(fix, key)
                        r2.parsed = extract_json(r2.text)
                        r2.attempts = attempt + 1
                        r2.cost_usd = (r2.cost_usd or 0) + (resp.cost_usd or 0) or None
                        resp = r2
                    except Exception:
                        pass
        # a validator checks the parsed JSON, or the text itself when the request is not JSON.
        # On a model API an invalid answer gets one repair attempt that names the problem.
        if validate is not None and (resp.parsed is not None if req.expect_json else bool((resp.text or "").strip())):
            problem = validate(resp.parsed if req.expect_json else resp.text)
            if problem and is_live:
                fix = LLMRequest(role=req.role, system=req.system,
                                 user=req.user + "\n\nYour previous reply could not be used: " + str(problem)[:600]
                                 + "\nReply again, complete and corrected, in the required output form.",
                                 expect_json=req.expect_json, tag=req.tag + ":repair",
                                 max_output_tokens=req.max_output_tokens, temperature=req.temperature,
                                 salt=req.salt, meta=req.meta)
                try:
                    r2 = prov.complete(fix, key)
                    r2.attempts = resp.attempts + 1
                    r2.cost_usd = (r2.cost_usd or 0) + (resp.cost_usd or 0) or None
                    if req.expect_json:
                        r2.parsed = extract_json(r2.text)
                    p2 = validate(r2.parsed if req.expect_json else r2.text)
                    if not p2:
                        resp, problem = r2, ""
                    else:
                        resp.attempts += 1
                        problem = p2
                except Exception:
                    pass
            if problem:
                resp.parse_error = f"validation: {problem}"
        if is_live:
            with self._lock:
                self.calls_made += resp.attempts
                if resp.cost_usd:
                    self.usd_spent += resp.cost_usd
                self._save_state()
        return resp

    def call(self, req: LLMRequest, validate: Callable | None = None) -> LLMResponse:
        hit = self.cached(req)
        if hit is not None:
            if req.expect_json and hit.parsed is None and not hit.parse_error:
                try:
                    hit.parsed = extract_json(hit.text)
                except JSONExtractError as e:
                    hit.parse_error = str(e)
            self._log(req, hit, "cache")
            return hit
        chain = self.providers_for(req.role)
        skipped: list[dict] = []
        resp: LLMResponse | None = None
        for n, prov in enumerate(chain):
            last = n == len(chain) - 1
            key = req.key(prov.identity)
            if prov.name in self.down:
                why = "skipped for this run: " + self.down[prov.name]
                if last:
                    raise ProviderError(f"no provider can answer {req.role} {req.tag}: "
                                        + "; ".join(f"{x['provider']}: {x['reason']}" for x in skipped
                                                    + [{"provider": prov.name, "reason": why}]))
                skipped.append({"provider": prov.name, "model": prov.model, "reason": why})
                continue
            try:
                resp = self._ask(prov, req, key, validate)
            except Pending:
                self._log(req, None, "pending", prov=prov)
                raise
            except ProviderError as e:
                reason = self._error_reason(e)
                dead = self._down_reason(e)
                if dead:
                    with self._lock:
                        self.down[prov.name] = dead
                    reason = dead
                self._log(req, None, "error" if last else "failover", str(e), prov=prov)
                if last:
                    if skipped:
                        e.args = (f"{e} [earlier providers skipped: "
                                  + "; ".join(f"{x['provider']}: {x['reason']}" for x in skipped) + "]",)
                    raise
                skipped.append({"provider": prov.name, "model": prov.model, "reason": reason})
                continue
            problem = self._unusable(req, resp)
            if problem and not last:
                skipped.append({"provider": prov.name, "model": prov.model, "reason": problem})
                self._log(req, resp, "failover", problem, prov=prov)
                resp = None
                continue
            resp.failover = skipped
            # only cache answers that parsed (or that were not meant to be JSON)
            if (not req.expect_json or resp.parsed is not None) and (resp.text or "").strip():
                write_json(self._cache_path(key), {
                    "request": req.to_record(), "response": resp.to_record(),
                    "provider_identity": prov.identity, "saved": utcnow()})
            if skipped:
                with self._lock:
                    self.failovers += 1
            self._log(req, resp, "ok" if not resp.parse_error else "parse_error", resp.parse_error, prov=prov)
            return resp
        raise ProviderError(f"no provider answered {req.role} {req.tag}")   # unreachable: chain is never empty

    def _needs_live(self, req: LLMRequest) -> bool:
        return self.providers_for(req.role)[0].kind in self.LIVE and self.cached(req) is None

    def call_many(self, reqs: list[LLMRequest], validate: Callable | None = None,
                  allow_pending: bool = False) -> list[LLMResponse | None]:
        """Run many independent requests.

        Pending queue items are collected; if any remain, ``Pending`` is raised
        after every other request has been tried (so one export holds the whole
        batch).  With ``allow_pending=True`` the pending slots are returned as
        ``None`` instead.
        """
        results: list[LLMResponse | None] = [None] * len(reqs)
        pending: list[str] = []
        live_idx: list[int] = []
        lock = threading.Lock()

        def run_one(i: int, errors: list | None = None) -> None:
            r = reqs[i]
            try:
                results[i] = self.call(r, validate)
            except Pending as p:
                with lock:
                    pending.extend(p.keys)
            except BudgetExceeded as e:
                if errors is None:
                    raise
                errors.append(e)
            except ProviderError as e:   # e.g. a queue request the operator skipped
                if errors is not None:
                    errors.append(e)
                results[i] = LLMResponse(text="", parse_error=f"provider error: {e}", key=self.key_for(r))
                if "skipped by the queue operator" not in str(e):
                    with self._lock:
                        self.error_count += 1

        for i, r in enumerate(reqs):
            if self._needs_live(r):
                live_idx.append(i)
            else:
                run_one(i)
        if live_idx:
            conc = max(1, int(self.cfg.get("budget", {}).get("concurrency", 4)))
            errors: list[Exception] = []
            with ThreadPoolExecutor(max_workers=conc) as ex:
                list(ex.map(lambda i: run_one(i, errors), live_idx))
            hard = [e for e in errors if isinstance(e, BudgetExceeded)]
            if hard:
                raise hard[0]
            if errors and len(errors) == len(live_idx):
                raise errors[0]
        if pending and not allow_pending:
            raise Pending(pending)
        return results

    def usage_summary(self) -> dict:
        return {"live_calls": self.calls_made, "estimated_usd": round(self.usd_spent, 4),
                "failovers": self.failovers, **({"providers_down": dict(self.down)} if self.down else {})}
