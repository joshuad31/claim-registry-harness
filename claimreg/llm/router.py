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
        self.calls_made = int(st.get("calls_made", 0))
        self.usd_spent = float(st.get("usd_spent", 0.0))

    # ------------------------------------------------------------------ #
    def provider_for(self, role: str) -> BaseProvider:
        name = self.cfg["roles"].get(role) or self.cfg.get("default_provider") or "openai"
        if name not in self._providers:
            pcfg = self.cfg["providers"].get(name)
            if pcfg is None:
                raise ProviderError(f"role {role!r} routed to unknown provider {name!r}")
            self._providers[name] = make_provider(name, pcfg, self.project_dir)
        return self._providers[name]

    def key_for(self, req: LLMRequest) -> str:
        return req.key(self.provider_for(req.role).identity)

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / key[:2] / f"{key}.json"

    def cached(self, req: LLMRequest) -> LLMResponse | None:
        """The stored answer for this exact request.  With ``cache_fallback_providers`` set (e.g.
        ["queue"]), an answer stored under one of those providers is reused when the role has since
        been routed elsewhere: a run can switch provider and ask only what is still missing.  The
        reused answer keeps its original provider and model in the record."""
        key = self.key_for(req)
        rec = read_json(self._cache_path(key))
        if not rec:
            for name in self.cfg.get("cache_fallback_providers", []) or []:
                pcfg = self.cfg["providers"].get(name)
                if not pcfg:
                    continue
                if name not in self._providers:
                    self._providers[name] = make_provider(name, pcfg, self.project_dir)
                alt = self._providers[name].identity
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

    def _log(self, req: LLMRequest, resp: LLMResponse | None, status: str, err: str = "") -> None:
        row = {
            "time": utcnow(), "status": status, "role": req.role, "tag": req.tag,
            "key": resp.key if resp else self.key_for(req),
            "provider": resp.provider if resp else self.provider_for(req.role).name,
            "model": resp.model if resp else self.provider_for(req.role).model,
            "cached": bool(resp and resp.cached),
            "system_sha256": sha256_text(req.system)[:16],
            "user_sha256": sha256_text(req.user)[:16],
            "response_sha256": sha256_text(resp.text)[:16] if resp else "",
            "usage": resp.usage if resp else {}, "cost_usd": resp.cost_usd if resp else None,
            "error": err[:500],
        }
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
        prov = self.provider_for(req.role)
        key = req.key(prov.identity)
        is_live = prov.kind in ("openai", "anthropic")
        if is_live:
            with self._lock:
                self._check_budget()
        retries = int(self.cfg.get("budget", {}).get("retries", 2))
        attempt = 0
        resp: LLMResponse | None = None
        while True:
            attempt += 1
            try:
                resp = prov.complete(req, key)
                break
            except Pending:
                self._log(req, None, "pending")
                raise
            except ProviderError as e:
                status = getattr(e, "status", None)
                transient = status in (0, 408, 409, 425, 429, 500, 502, 503, 504, 529)
                if transient and attempt <= retries:
                    backoff_sleep(attempt)
                    continue
                self._log(req, None, "error", str(e))
                raise
        resp.attempts = attempt
        if req.expect_json:
            try:
                resp.parsed = extract_json(resp.text)
            except JSONExtractError as e:
                resp.parse_error = str(e)
                if is_live:
                    fix = LLMRequest(role=req.role, system=req.system,
                                     user=req.user + "\n\n" + JSON_REPAIR,
                                     expect_json=True, tag=req.tag + ":json-repair",
                                     max_output_tokens=req.max_output_tokens,
                                     temperature=req.temperature, salt=req.salt)
                    try:
                        r2 = prov.complete(fix, key)
                        r2.parsed = extract_json(r2.text)
                        r2.attempts = attempt + 1
                        resp = r2
                    except Exception:
                        pass
        if validate is not None and resp.parsed is not None:
            problem = validate(resp.parsed)
            if problem:
                resp.parse_error = f"validation: {problem}"
        if is_live:
            with self._lock:
                self.calls_made += resp.attempts
                if resp.cost_usd:
                    self.usd_spent += resp.cost_usd
                self._save_state()
        # only cache answers that parsed (or that were not meant to be JSON)
        if not req.expect_json or resp.parsed is not None:
            write_json(self._cache_path(key), {
                "request": req.to_record(), "response": resp.to_record(),
                "provider_identity": prov.identity, "saved": utcnow()})
        self._log(req, resp, "ok" if not resp.parse_error else "parse_error", resp.parse_error)
        return resp

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
        for i, r in enumerate(reqs):
            prov = self.provider_for(r.role)
            if prov.kind in ("openai", "anthropic") and self.cached(r) is None:
                live_idx.append(i)
                continue
            try:
                results[i] = self.call(r, validate)
            except Pending as p:
                pending.extend(p.keys)
            except ProviderError as e:   # e.g. a queue request the operator skipped
                results[i] = LLMResponse(text="", parse_error=f"provider error: {e}", key=self.key_for(r))
                if "skipped by the queue operator" not in str(e):
                    with self._lock:
                        self.error_count += 1
        if live_idx:
            conc = max(1, int(self.cfg.get("budget", {}).get("concurrency", 4)))
            errors: list[Exception] = []

            def run(i):
                try:
                    results[i] = self.call(reqs[i], validate)
                except BudgetExceeded as e:
                    errors.append(e)
                except ProviderError as e:
                    errors.append(e)
                    results[i] = LLMResponse(text="", parse_error=f"provider error: {e}",
                                             key=self.key_for(reqs[i]))
                    with self._lock:
                        self.error_count += 1

            with ThreadPoolExecutor(max_workers=conc) as ex:
                list(ex.map(run, live_idx))
            hard = [e for e in errors if isinstance(e, BudgetExceeded)]
            if hard:
                raise hard[0]
            if errors and len(errors) == len(live_idx):
                raise errors[0]
        if pending and not allow_pending:
            raise Pending(pending)
        return results

    def usage_summary(self) -> dict:
        return {"live_calls": self.calls_made, "estimated_usd": round(self.usd_spent, 4)}
