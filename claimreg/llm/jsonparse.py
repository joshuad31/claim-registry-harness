"""Robust extraction of one JSON value from model output."""

from __future__ import annotations

import json
import re
from typing import Any

_FENCE = re.compile(r"```(?:json|JSON)?\s*\n(.*?)\n?```", re.S)


class JSONExtractError(ValueError):
    pass


def _try(s: str):
    try:
        return True, json.loads(s)
    except Exception:
        return False, None


def _strip_trailing_commas(s: str) -> str:
    return re.sub(r",(\s*[}\]])", r"\1", s)


def extract_json(text: str) -> Any:
    """Return the most plausible JSON object/array contained in ``text``.

    Order: whole text; fenced ```json blocks (last first, since models often
    restate); then the longest raw-decodable value starting at a '{' or '['.
    """
    if text is None:
        raise JSONExtractError("empty response")
    t = text.strip()
    if not t:
        raise JSONExtractError("empty response")
    ok, v = _try(t)
    if ok:
        return v
    fences = _FENCE.findall(t)
    for block in reversed(fences):
        for cand in (block, _strip_trailing_commas(block)):
            ok, v = _try(cand.strip())
            if ok:
                return v
    dec = json.JSONDecoder()
    best = None
    best_len = -1
    for m in re.finditer(r"[\[{]", t):
        start = m.start()
        for cand in (t[start:], _strip_trailing_commas(t[start:])):
            try:
                v, end = dec.raw_decode(cand)
            except Exception:
                continue
            if end > best_len and isinstance(v, (dict, list)):
                best, best_len = v, end
            break
        if best_len > 0 and best_len > len(t) * 0.5:
            break
    if best is not None:
        return best
    raise JSONExtractError("no parseable JSON value found in response")


def as_list(v: Any, key: str | None = None) -> list:
    """Accept a bare list or an object wrapping a list under ``key`` (or any key)."""
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        if key and isinstance(v.get(key), list):
            return v[key]
        for val in v.values():
            if isinstance(val, list):
                return val
    return []
