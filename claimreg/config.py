"""Project configuration: defaults, deep merge, load and save.

A project directory holds one ``project.json``.  Anything not set there falls
back to ``DEFAULT_CONFIG``.  Every value that changes a scientific result is
recorded in each run's RUN-CONFIG.json, so two runs can always be compared.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .util import read_json, write_json

# Every model-facing role.  Each one may be routed to its own provider/model.
ROLES = [
    "indexer",               # ranked-index entries (optional)
    "archivist_writer",      # generates the Archivist custom prompt (optional)
    "investigator",          # writes quest questions
    "archivist",             # answers one source-grounded question from the corpus
    "coordinator",           # ACH_Eval assessment + feedback packet
    "frd_generator",         # query-response file -> candidate FRDs
    "frd_validator",         # blind source-only validation
    "unit_deriver",          # hypothesis -> coverage units
    "dictionary_reviewer",   # contextual-sense review (language layer)
    "transcoder",            # controlled-English rewrite (language layer)
    "witness_constructor",   # (question, validated FRD) -> witness
    "witness_auditor",       # independent two-direction fidelity audit
    "matcher_a",             # semantic matching pass A
    "matcher_b",             # semantic matching pass B (independent)
    "match_adjudicator",     # resolves A/B disagreements (labelled as model adjudication)
    "joint_checker",         # jointly-sufficient group approval
    "incompat_checker",      # witness-witness incompatibility approval
    "assessor",              # final ACH_Eval-style assessment over the witness registry
    "reporter",              # optional plain-language analyst summary
]

DEFAULT_CONFIG: dict[str, Any] = {
    "project": {
        "name": "Untitled investigation",
        "run_prefix": "RUN",
        "publishable": False,
    },
    "corpus": {
        # relative to the project directory unless absolute
        "source_dir": "01_CORPUS/source-files",
        "chunk_words": 320,
        "chunk_overlap_words": 40,
        "extensions": [".md", ".markdown", ".txt"],
    },
    "frame": {
        "header_file": "01_FRAME/header.md",
        "index_file": "01_FRAME/index.md",
        "archivist_prompt_file": "01_FRAME/archivist-custom-prompt.txt",
        "approval_note": "",
    },
    "providers": {
        "openai": {
            "type": "openai",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-5.5",
            "api_key_env": "OPENAI_API_KEY",
            "api_key_file": None,
            "max_output_tokens": 16000,
            "temperature": None,
            "timeout_s": 900,
            "json_mode": False,
            "price_per_mtok_in": 2.0,
            "price_per_mtok_out": 10.0,
        },
        "deepseek": {
            "type": "openai",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
            "api_key_env": "DEEPSEEK_API_KEY",
            "api_key_file": None,
            "max_output_tokens": 8000,
            "temperature": 0.2,
            "timeout_s": 900,
            "json_mode": False,
            "price_per_mtok_in": 0.3,
            "price_per_mtok_out": 1.2,
        },
        "anthropic": {
            "type": "anthropic",
            "base_url": "https://api.anthropic.com/v1",
            "model": "claude-opus-5-5",
            "api_key_env": "ANTHROPIC_API_KEY",
            "api_key_file": None,
            "max_output_tokens": 16000,
            "temperature": None,
            "timeout_s": 900,
            "price_per_mtok_in": 5.0,
            "price_per_mtok_out": 25.0,
        },
        "queue": {
            # Writes each request to <project>/queue/pending and waits for a
            # response file in <project>/queue/done.  Use it for NotebookLM by
            # hand, any chat UI, or an agent acting as the model.
            "type": "queue",
            "dir": "queue",
            "model": "queue-operator",
            "operator_note": "",
        },
        "mock": {"type": "mock", "model": "mock-deterministic"},
        "replay": {"type": "replay", "model": "replay-cache-only"},
        "local": {
            # Deterministic offline analyst.  It answers every role from the
            # supplied text with explicit lexical and structural rules, so a
            # project can run from an empty folder to a finished report with no
            # network, key or queue.  It is not a language model; see
            # claimreg/llm/local.py for exactly what it does and does not do.
            "type": "local",
            "model": "local-rules-v1.8",
        },
    },
    # role -> provider name (a key of "providers").  The local engine is the
    # default so that `cr run` can never stall waiting for model answers.
    "roles": {r: "local" for r in ROLES},
    "default_provider": "local",
    "budget": {
        "max_calls": 3000,
        "max_usd": 100.0,
        "concurrency": 4,
        "retries": 2,
    },
    "quest": {
        "round_size": 5,              # newly saved usable QIDs per round (spec: 5-6)
        "max_rounds": 12,             # operational ceiling, not a scientific stop
        "gauge": 64,                  # ACH_Eval allocation gauge G
        "axes": "header",             # use the axes the header defines
        "feedback_deadline_qids": 8,
        "archivist_context_words": 9000,
        "named_source_words": 4500,   # retrieved words per named source
        "other_chunks": 6,            # extra corpus chunks the Archivist may cite
        "require_ab_coverage_for_branch2": True,
    },
    "frd": {
        "max_per_response": 4,        # Problems note: every proper response -> <=4 FRDs
        "validator_source_words": 14000,
        "quote_min_ratio": 0.92,      # fuzzy fallback threshold for long quotations
        "quote_gate": "block",        # block: an FRD whose quotation is not found in its source is not READY
    },
    "retention": {
        "keep_fraction": 0.80,        # never archive more than 20% of READY FRDs
        "small_corpus_mb": 1.0,
        "large_corpus_mb": 12.0,
        "small_budget_pct": 25.0,     # FRD db <= 25% of corpus when corpus <= 1 MB
        "large_budget_pct": 8.0,      # FRD db <= 8% of corpus when corpus >= 12 MB
        "archive_redundant_first": True,
    },
    "witness": {
        "raw_ceiling": 60,            # owner-set (Sept 6) raw witness maximum
        "transcoded_ceiling": 80,     # owner-set transcoded maximum
        "allow_ceiling_exception": True,
        "exception_ceiling": 80,      # recorded per-pair exception when 60 loses meaning
        "max_revisions": 1,
        "cluster_best": False,        # spec 24.4 experiment, off by default
    },
    "language": {
        "mode": "off",                # off | labels  (labels = dictionary + transcoder)
        "min_sentences": 3,           # three distinct example sentences per active sense
        "max_candidates": 40,
        "dictionary_file": None,      # optional frozen dictionary to reuse (spec 22.2)
    },
    "matching": {
        "shortlist_k": 30,             # REQUIRED_SUPPORT and CONTEXTUAL_CONSTRAINT units
        "shortlist_k_secondary": 15,   # ADVERSE_TEST and CORROBORATING_EXPECTATION units
        "batch_size": 15,
        "exhaustive_threshold": 45,   # match every witness when there are this few
        "dispute_policy": "adjudicate",   # adjudicate | abstain
        "synonyms": [],               # e.g. [["PTX", "pentoxifylline"]]: shortlist only, never shown to the matcher
        "one_pass_policy": "abstain",  # a pass left unanswered (cr queue skip): abstain | accept (labelled ONE_PASS_ONLY)
        "qualify": True,
    },
    "coverage": {
        "max_sets": 200,
        "max_states": 3000,
        "max_options_per_unit": 12,
        "max_group_size": 3,
        "max_joint_candidates": 10,
        "max_incompat_pairs": 200,    # witness pairs sent to the incompatibility check
        "constraint_veto": True,      # a member contradicting a constraint unit invalidates a set
    },
    "crux": {
        "diagnostic_top_n": 15,
        "completion_matching": True,  # judge crux-tested witnesses against rival units
        "diagnostic_units_per_rival": 8,  # shortlist size for diagnostic (extended-review) witnesses
    },
    "assess": {"enabled": True},
    "report": {"max_words": 3900, "llm_summary": True},
}


def deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(project_dir: str | Path) -> dict:
    project_dir = Path(project_dir)
    user = read_json(project_dir / "project.json", default={}) or {}
    cfg = deep_merge(DEFAULT_CONFIG, user)
    # any role not routed falls back to the "default_provider" if one is named
    dp = user.get("default_provider")
    if dp:
        for r in ROLES:
            if r not in (user.get("roles") or {}):
                cfg["roles"][r] = dp
    cfg["_project_dir"] = str(project_dir.resolve())
    return cfg


def save_user_config(project_dir: str | Path, user_cfg: dict) -> None:
    write_json(Path(project_dir) / "project.json", user_cfg)


def resolve_path(cfg: dict, p: str | None) -> Path | None:
    if not p:
        return None
    pp = Path(p)
    if not pp.is_absolute():
        pp = Path(cfg["_project_dir"]) / pp
    return pp


def scientific_config(cfg: dict) -> dict:
    """The part of the config that can change results (recorded per run)."""
    keep = ["quest", "frd", "retention", "witness", "language", "units", "matching",
            "coverage", "crux", "assess", "report", "roles"]
    out = {k: copy.deepcopy(cfg.get(k)) for k in keep}
    prov = {}
    for name, p in cfg.get("providers", {}).items():
        prov[name] = {k: v for k, v in p.items()
                      if k not in ("api_key_file", "api_key_env")}
    out["providers"] = prov
    return out
