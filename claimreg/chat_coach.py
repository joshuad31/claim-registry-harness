"""Resumable frame coaching in the host assistant's chat, without a terminal interview.

The command is an adapter for the assistant. Questions and choices are shown in chat; the
assistant submits the person's actual replies. This is an acceptance record, not authentication.
"""
from __future__ import annotations

import json
import math
import re
import shutil
import uuid
from pathlib import Path

from . import frame_gate as fg
from .header import normalize_hypothesis_ids, parse_header
from .util import read_json, read_text, sha256_text, utcnow, write_json

SESSION = "coaching-session.json"


class PreparationNeeded(ValueError):
    def __init__(self, message, detail=""):
        super().__init__(message)
        self.detail = detail


def normalize_draft(text, question=""):
    """Repair only unambiguous layout; never invent or rewrite a hypothesis."""
    text, _ = normalize_hypothesis_ids(fg._norm(text))
    frame = parse_header(text)
    missing = [a for a in frame["axes"] if a["axis_id"] not in fg.axis_spans(text)]
    if missing and len(frame["axes"]) == 1 and question.strip():
        # A single-axis draft sometimes has its table directly under 'Frozen hypotheses'.
        # Insert the missing section inside that block, keeping all the existing content.
        from .header import _sections
        headings = [(s, e) for level, h, s, e in _sections(text)
                    if level <= 3 and re.search(r"hypotheses|competing|rival", h, re.I)
                    and all(hyp["id"] in text[s:e] for hyp in missing[0]["hypotheses"])]
        if headings:
            start = headings[-1][0]
            at = text.find("\n", start) + 1
            text = text[:at] + f"\n### Axis {missing[0]['axis_id'][1:]}\n\n{question.strip()}\n" + text[at:]
            frame = parse_header(text)
    for axis in frame["axes"]:
        if axis["axis_id"] not in fg.axis_spans(text) or not axis.get("question"):
            raise PreparationNeeded("I need to finish preparing the saved research question before we review it.",
                                    "Add an explicit question section for each axis, preserving its statements and scope.")
        if len(axis["hypotheses"]) < 2 or any(not h["statement"] for h in axis["hypotheses"]):
            raise PreparationNeeded("The saved draft is missing one or more competing explanations. I'll fix the draft first.",
                                    "Each parsed hypothesis needs its full statement in the hypothesis table.")
    return text


def _question(project):
    path = project / "01_FRAME" / "question.md"
    text = read_text(path) if path.is_file() else ""
    match = re.search(r"^##\s+(?:What I want to decide|What I want to find out|Research question|Question)\s*\n"
                      r"(.*?)(?=^##\s|\Z)", text, re.I | re.M | re.S)
    return match.group(1).strip() if match and not match.group(1).strip().startswith("REPLACE") else ""


def inspect_draft(project, header=None):
    """Read-only preflight; also useful before creating any coaching session."""
    project = Path(project).resolve()
    if not (project / "project.json").is_file():
        raise PreparationNeeded("I need to open the research project before we can review its question.")
    if (project / "01_FRAME" / "frame.json").exists():
        raise PreparationNeeded("This project has two saved question definitions. I'll reconcile them before asking you to approve one.",
                                "01_FRAME/frame.json overrides the Markdown header; reconcile deliberately, not by deleting it silently.")
    paths = fg._configured(project)
    source = Path(header).resolve() if header else paths["header"]
    if not source.is_file() and not header:
        source = project / "01_FRAME" / "header-DRAFT.md"
    if not source.is_file():
        raise PreparationNeeded("The research draft hasn't been saved yet. I'll prepare it before we start the review.",
                                "Run the frame preparation operation, then resume coaching from header-DRAFT.md.")
    if not paths["index"].is_file() or not read_text(paths["index"]).strip():
        raise PreparationNeeded("I need the map of your sources before I can explain what this comparison can test.",
                                "Prepare the source index, then resume coaching.")
    text = normalize_draft(read_text(source), _question(project))
    return {"text": text, "source": str(source), "paths": paths, "frame": parse_header(text)}


def _fingerprints(paths):
    return {str(p): sha256_text(read_text(p)) if Path(p).is_file() else None for p in paths}


def _save(project, state):
    state["revision"] += 1
    state["updated"] = utcnow()
    write_json(project / "01_FRAME" / SESSION, state)


def _fresh(state):
    if _fingerprints(state["inputs"]) != state["inputs"]:
        raise PreparationNeeded("The saved question or source map changed while we were reviewing it. I'll refresh the review before you approve anything.",
                                "Restart coaching against the current files; do not replay approval from the earlier review.")


def begin(project, header=None, only=None, name=None):
    prepared = inspect_draft(project, header)
    text, frame = prepared["text"], prepared["frame"]
    old = fg.load_certificate(project) or {}
    stale = fg.unaccepted_axes(text, old)
    records = {a: r for a, r in (old.get("axes") or {}).items() if a not in stale and a != only}
    order = [a["axis_id"] for a in frame["axes"] if a["axis_id"] not in records and (not only or a["axis_id"] == only)]
    if only and not order:
        raise PreparationNeeded("That research question isn't in this draft. I'll use the questions actually saved in the project.")
    state = {"version": 1, "id": uuid.uuid4().hex, "revision": 0, "text": text,
             "source": prepared["source"], "order": order, "position": 0,
             "phase": "purpose" if order else "completed", "answers": {}, "records": records,
             "who": {}, "name": name or old.get("name") or "the researcher", "events": [],
             "inputs": _fingerprints([prepared["source"], prepared["paths"]["header"], prepared["paths"]["index"],
                                       project / "project.json"])}
    _save(project, state)
    return state


def _axis(state):
    aid = state["order"][state["position"]]
    return next(a for a in parse_header(state["text"])["axes"] if a["axis_id"] == aid)


def _evidence(project, state):
    paths = fg._configured(project)
    evidence = read_text(paths["index"])[:60000]
    findings, basis = fg.frd_digest(project, _axis(state)["axis_id"])
    return evidence + ("\n\nValidated findings:\n" + findings if findings else ""), \
        "the source map (orientation, not primary evidence)" + (" and " + basis if findings else "")


def _original(axis):
    return {"label": "Keep the current wording", "question": axis["question"],
            "statements": {h["id"]: h["statement"] for h in axis["hypotheses"]},
            "changes": [], "cannot_be_tested": [], "rival_held_by": "", "leaves_out": ""}


def _candidate_text(state, candidate):
    axis = _axis(state)
    statements = candidate.get("statements", {})
    if not isinstance(statements, dict) or set(statements) != {h["id"] for h in axis["hypotheses"]}:
        raise PreparationNeeded("The proposed wording omitted an explanation. I'll restore the complete comparison before showing it.")
    if not isinstance(candidate.get("question"), str) or not candidate["question"].strip():
        raise PreparationNeeded("The proposed comparison needs its research question before it can be reviewed.")
    if any(not isinstance(value, str) or len(value.strip()) <= 30 for value in statements.values()):
        raise PreparationNeeded("One proposed explanation is incomplete. I'll keep the full wording for your review.")
    text = fg.replace_axis(state["text"], axis["axis_id"], candidate["question"], candidate["statements"])
    return normalize_draft(text)


def prepare(project, state, model=None):
    axis = _axis(state)
    candidates = [_original(axis)]
    evidence, basis = _evidence(project, state)
    notes = []
    preferred = state["answers"].get("preferred")
    if model:
        who = {**state["who"], **state["answers"]}
        try:
            restated = fg.restate(model, fg._own(who), axis["question"], candidates[0]["statements"], evidence)
            if (restated["question"], restated["statements"]) != (axis["question"], candidates[0]["statements"]):
                candidates.append({**restated, "label": "Clarify the current wording"})
        except Exception:
            notes.append("A suggested clarification wasn't available. The original wording is still available for review.")
        if preferred:
            try:
                candidates += fg.ladder(model, who, preferred, axis["question"], candidates[0]["statements"], evidence)[:3]
            except Exception:
                notes.append("Alternative wordings weren't available; we can discuss edits here instead.")
    valid = []
    for candidate in candidates:
        try:
            _candidate_text(state, candidate)
        except (ValueError, KeyError, TypeError):
            continue
        candidate["forecast"] = fg.forecast(model, candidate["question"], candidate["statements"],
                                             parse_header(state["text"])["gauge"], evidence, "chat-coach") if model else {"ok": 0, "calls": []}
        valid.append(candidate)
    state.update(candidates=valid, forecast_basis=basis, notes=notes, phase="options", model_review=bool(model))


def _checked_reading(reading, fallback, ids, gauge):
    if not isinstance(reading, dict):
        raise ValueError("Incomplete review")
    out = dict(fallback)
    for field in ("if_it_wins_you_may_say", "you_may_not_say", "left_out", "a_critic_will_say", "conflicts"):
        value = reading.get(field, fallback.get(field, []))
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            raise ValueError("Invalid review field")
        out[field] = value
    if not out["if_it_wins_you_may_say"]:
        raise ValueError("Missing interpretation")
    holder = reading.get("rival_is_held_by", fallback["rival_is_held_by"])
    out["rival_is_held_by"] = holder if isinstance(holder, str) else fallback["rival_is_held_by"]
    worst = reading.get("worst_case", {})
    if not isinstance(worst, dict):
        raise ValueError("Invalid worst-case review")
    alloc = worst.get("allocations") or {}
    if alloc and (not isinstance(alloc, dict) or set(alloc) != set(ids)
                  or any(type(v) is not int or v < 0 for v in alloc.values()) or sum(alloc.values()) != gauge):
        alloc = {}  # Do not present malformed numerical forecasts to the person.
    conclusion = worst.get("then_you_would_have_to_say")
    out["worst_case"] = {"allocations": alloc, "then_you_would_have_to_say":
                         conclusion if isinstance(conclusion, str) and conclusion.strip() else
                         fallback["worst_case"]["then_you_would_have_to_say"]}
    return out


def _review(project, state, model=None):
    axis = _axis(state)
    candidate = state["candidates"][state["selected"]]
    text = state.get("revised_text") or _candidate_text(state, candidate)
    reviewed_axis = next(a for a in parse_header(text)["axes"] if a["axis_id"] == axis["axis_id"])
    # A fallback states general limits; it never invents a corpus-specific conclusion or score.
    reading = {"if_it_wins_you_may_say": ["The reviewed sources favor an explanation as it is worded, within the stated scope."],
               "you_may_not_say": ["That a favored explanation is proven for every individual or for outcomes outside this question."],
               "worst_case": {"allocations": {}, "then_you_would_have_to_say": state["answers"]["concede"]},
               "rival_is_held_by": "Not independently checked in this review", "left_out": [],
               "a_critic_will_say": [], "conflicts": []}
    steps = {"review": "general limits only; no model review requested"}
    if model:
        fallback = reading
        try:
            if state["answers"].get("preferred"):
                block = json.dumps(fg.reviewed_context(reviewed_axis), ensure_ascii=False)
                result = fg.back_translate(model, block, state["answers"]["preferred"], candidate["forecast"],
                                            parse_header(text)["gauge"])
            else:
                result = model("neutral-review", fg.SYSTEM,
                                "Review this research comparison without favoring any explanation. Return the plain-language "
                                "fields if_it_wins_you_may_say (what a result could support), you_may_not_say, "
                                "worst_case (allocations may be empty; then_you_would_have_to_say), rival_is_held_by, "
                                "left_out, a_critic_will_say, conflicts. Use arrays of strings except the named object and string. "
                                "Do not diagnose a person or invent evidence. Comparison: " + json.dumps(fg.reviewed_context(reviewed_axis)), "")
            reading = _checked_reading(result, fallback, candidate["statements"], parse_header(text)["gauge"])
            steps["review"] = "ok"
        except Exception:
            state["notes"].append("The detailed model review wasn't available. The review below uses general limits; no research result is claimed.")
    state.update(reviewed_text=text, reviewed_axis=reviewed_axis, reading=reading, model_steps=steps,
                 review_position=0, confirmations=[], phase="wording")
    state["intent_check"] = {"match": None, "gap": "Not independently checked; discuss the stated goal alongside the wording."}
    if model:
        try:
            state["intent_check"] = fg.judge(model, state["who"]["goal"], reading["if_it_wins_you_may_say"])
        except Exception:
            pass


def packet(state):
    phase = state["phase"]
    out = {"status": "completed" if phase == "completed" else "awaiting_reply", "step": phase,
           "revision": state["revision"], "session_id": state["id"], "can_accept": phase == "approval",
           "for_the_assistant": "Keep this conversation in chat. Ask one plain question at a time; use the user's actual replies, "
                                "including relevant replies already in the conversation. Do not open a terminal, ask for retyping, "
                                "show internal IDs or JSON, invent replies, or approve on the user's behalf."}
    prompts = {
        "purpose": "What would you like this research to help you understand or do?",
        "preference": "Do you currently lean toward one explanation, or are you keeping an open mind?",
        "experience": "What experiences or observations brought you to this question? It's fine if you don't have a particular view yet.",
        "concede": "If the evidence points another way, what would you be willing to change your mind about?",
        "prepare": "I have enough context to help you review the comparison. I'll prepare the wording and its limits now.",
        "options": "Would you like to keep the current wording, consider an alternative, or make a change?",
        "wording": "Does this explanation say what you mean, or would you like to change it?",
        "scope": "Are these the people, circumstances, and outcomes you want this research to cover?",
        "consequences": "Are you comfortable with these limits and the possibility that the evidence may not settle the question?",
        "approval": "Are you ready to use this exact wording for the research run, or would you like changes?",
        "completed": "Your research wording is reviewed and saved. We can continue preparing the run."}
    out["question"] = prompts[phase]
    if phase not in ("purpose", "completed"):
        axis = state["reviewed_axis"] if phase in ("wording", "scope", "consequences", "approval") else _axis(state)
        out["comparison"] = {"question": axis["question"], "explanations": axis["hypotheses"]}
    action = "prepare" if phase == "prepare" else "select" if phase == "options" else "accept" if phase == "approval" else "reply"
    if phase != "completed":
        out["next_request"] = {"action": action, "base_payload": {"session_id": state["id"], "revision": state["revision"]},
                               "requires_actual_user_reply": phase != "prepare"}
    if phase == "prepare":
        out["for_the_assistant"] += (" Run coach --action prepare to use the saved draft; add --model-review only for "
                                     "configured model-assisted alternatives/forecasts (may incur usage). Never represent "
                                     "an index summary or forecast as a verified finding.")
    if phase == "options":
        out["options"] = state["candidates"]
        out["forecast_basis"] = state["forecast_basis"]
        out["notes"] = state.get("notes", [])
        out["for_the_assistant"] += " Explain choices in words; do not ask the user to type hypothesis IDs or option codes."
    if phase == "wording":
        h = state["reviewed_axis"]["hypotheses"][state["review_position"]]
        out["show"] = {"explanation": h["statement"], "title": h.get("title", ""),
                       "assumptions": h.get("assumptions", ""), "evidence_against": h.get("falsification", ""),
                       "evidence_for": h.get("corroboration", "")}
    elif phase == "scope":
        out["show"] = {"scope": state["reviewed_axis"].get("scope", ""), "limits": state["reviewed_axis"].get("boundary", "")}
    elif phase in ("consequences", "approval"):
        candidate = state["candidates"][state["selected"]]
        out["show"] = {"question": state["reviewed_axis"]["question"], "explanations": state["reviewed_axis"]["hypotheses"],
                       "scope": state["reviewed_axis"].get("scope", ""), "limits": state["reviewed_axis"].get("boundary", ""),
                       "meaning_and_limits": state["reading"], "forecast": candidate["forecast"],
                       "user_goal": state["who"]["goal"], "fit_with_user_goal": state["intent_check"],
                       "forecast_basis": state["forecast_basis"], "changes": candidate.get("changes", []),
                       "cannot_be_tested": candidate.get("cannot_be_tested", []), "notes": state.get("notes", []),
                       "forecast_explanation": "An advisory estimate of how evidence might be allocated, not a result or a probability. "
                                               "If ok is zero, no numerical forecast was made."}
        out["for_the_assistant"] += " Explain the scope, meaningful outcomes, omissions, rival, and uncertainty before requesting approval."
    return out


def _reply(state, data):
    phase, text = state["phase"], data["text"].strip()
    state["events"].append({"step": phase, "text": text, "at": utcnow(), "origin": "user_reply_in_chat"})
    if phase == "purpose":
        state["who"] = {"motivation": text, "goal": text}
        state["phase"] = "preference"
    elif phase == "preference":
        choices = {h["id"] for h in _axis(state)["hypotheses"]}
        if "choice" not in data or (data["choice"] is not None and
                                    (not isinstance(data["choice"], str) or data["choice"] not in choices)):
            raise PreparationNeeded("I'll clarify whether you favor an explanation before going on.",
                                    "Record choice as the selected hypothesis ID, or null for an open mind; do not choose for the user.")
        state["answers"]["preferred"] = data["choice"]
        state["phase"] = "experience"
    elif phase in ("experience", "concede"):
        state["answers"][phase] = text
        state["phase"] = "concede" if phase == "experience" else "prepare"
    elif phase in ("wording", "scope", "consequences"):
        if data.get("confirmed") is not True:
            raise PreparationNeeded("Let's make the changes you want before continuing.", "Use revise to stage changes; no approval has been recorded.")
        state["confirmations"].append({"item": phase, "shown": packet(state).get("show", {}), "typed": text,
                                       "origin": "user_reply_in_chat", "at": utcnow()})
        if phase == "wording":
            state["review_position"] += 1
            if state["review_position"] == len(state["reviewed_axis"]["hypotheses"]):
                state["phase"] = "scope" if any(state["reviewed_axis"].get(k) for k in ("scope", "boundary")) else "consequences"
        else:
            state["phase"] = "consequences" if phase == "scope" else "approval"
    else:
        raise PreparationNeeded("I'll finish the current review step before recording that answer.")


def _accept(project, state, data):
    if state["phase"] != "approval" or data.get("confirmed") is not True:
        raise PreparationNeeded("We haven't finished reviewing the wording and its limits yet. Let's do that before approving it.")
    axis = state["reviewed_axis"]
    candidate = state["candidates"][state["selected"]]
    text = state["reviewed_text"]
    g = parse_header(text)["gauge"]
    original = _axis(state)
    entry = lambda text: {"text": text, "origin": "reviewed_in_chat"}
    record = {"axis_id": axis["axis_id"], "name": axis.get("name", ""), "gauge": g,
              "preferred": state["answers"].get("preferred") or "", "target": math.ceil(fg.TARGET_SHARE * g),
              "experience": entry(state["answers"]["experience"]), "intent": entry(state["who"]["goal"]),
              "concede": entry(state["answers"]["concede"]),
              "typed": {"question": entry(original["question"]),
                        "statements": {h["id"]: entry(h["statement"]) for h in original["hypotheses"]}},
              "restated": {"question": axis["question"], "statements": {h["id"]: h["statement"] for h in axis["hypotheses"]},
                           "changes": candidate.get("changes", []), "cannot_be_tested": candidate.get("cannot_be_tested", [])},
              "forecast": candidate["forecast"], "forecast_basis": state["forecast_basis"], "ladder": state["candidates"],
              "back_translation": state["reading"], "judge": state["intent_check"], "read": [], "model_steps": state["model_steps"],
              "accepted": state["confirmations"] + [{"item": "Use this exact wording", "typed": data["text"],
                                                       "shown": packet(state)["show"], "at": utcnow(), "origin": "user_reply_in_chat"}],
              "reviewed_context": fg.reviewed_context(axis), "channel": "chat", "accepted_at": utcnow()}
    # Preserve previous files before promoting the reviewed draft; never accept by copying a draft alone.
    backup = project / "99_ARCHIVE" / "frame-coaching" / state["id"]
    backup.mkdir(parents=True, exist_ok=True)
    for path in [fg.header_path(project), project / "01_FRAME" / fg.CERT_JSON, project / "01_FRAME" / fg.CERT_MD]:
        target = backup / path.name
        if path.is_file() and not target.exists():
            shutil.copyfile(path, target)
    state["records"][axis["axis_id"]] = record
    cert = {"version": 3, "channel": "chat", "project": project.name, "name": state["name"],
            "who": state["who"], "axes": state["records"]}
    fg._write(project, cert, text, False)
    state["text"] = fg._norm(read_text(fg.header_path(project)))
    state["inputs"] = _fingerprints(state["inputs"])
    state["position"] += 1
    state["answers"] = {}
    state.pop("revised_text", None)
    state["phase"] = "completed" if state["position"] == len(state["order"]) else "preference"


def act(project, action="status", data=None, model=None, header=None, only=None, name=None):
    project = Path(project).resolve()
    path = project / "01_FRAME" / SESSION
    if action == "restart" or not path.is_file():
        if action not in ("status", "restart"):
            raise PreparationNeeded("Let's start the chat review before recording answers.")
        return packet(begin(project, header, only, name))
    state = read_json(path)
    _fresh(state)
    if action == "status":
        return packet(state)
    if state["phase"] == "completed":
        raise PreparationNeeded("This wording review is already saved. We can continue preparing the run, or start a new review if you want changes.")
    if not isinstance(data, dict) or data.get("revision") != state["revision"] or data.get("session_id") != state["id"]:
        raise PreparationNeeded("That answer belongs to an earlier review step. I'll show you the current step before continuing.",
                                "Read coach status and submit its revision with the actual user reply.")
    if action in ("reply", "select", "revise", "accept") and (not isinstance(data.get("text"), str) or not data["text"].strip()):
        raise PreparationNeeded("I'll record your own reply before continuing. Nothing has been approved.")
    if action == "reply":
        _reply(state, data)
    elif action == "prepare":
        if state["phase"] != "prepare":
            raise PreparationNeeded("I'll finish discussing your research goal before preparing the wording review.")
        prepare(project, state, model)
    elif action == "select":
        if state["phase"] != "options" or type(data.get("choice")) is not int or not 0 <= data["choice"] < len(state["candidates"]):
            raise PreparationNeeded("I'll show the available wording choices again before selecting one.")
        state["selected"] = data["choice"]
        state["events"].append({"step": "options", "text": data["text"], "at": utcnow(), "origin": "user_reply_in_chat"})
        _review(project, state, model)
    elif action == "revise":
        if state["phase"] not in ("options", "wording", "scope", "consequences", "approval"):
            raise PreparationNeeded("Let's reach the wording review before making this change.")
        candidate = data.get("candidate") or {}
        if data.get("draft_file"):
            text = normalize_draft(read_text(Path(data["draft_file"])), _question(project))
            revised = parse_header(text)
            current = parse_header(state["text"])
            if revised["gauge"] != current["gauge"]:
                raise PreparationNeeded("The revision changed the assessment settings. I'll start a fresh review before using that change.")
            if [a["axis_id"] for a in revised["axes"]] != [a["axis_id"] for a in current["axes"]]:
                raise PreparationNeeded("The revision changed which research questions are included. I'll restart a complete review for that change.")
            aid = _axis(state)["axis_id"]
            for old, new in zip(current["axes"], revised["axes"]):
                if old["axis_id"] != aid and fg.reviewed_context(old) != fg.reviewed_context(new):
                    raise PreparationNeeded("Other research questions changed too. I'll review those changes together in a fresh session.")
            revised_axis = next(a for a in revised["axes"] if a["axis_id"] == aid)
            candidate = {**_original(revised_axis), "changes": data.get("changes", [])}
            _candidate_text(state, candidate)
            state["revised_text"] = text
        else:
            _candidate_text(state, candidate)
            state.pop("revised_text", None)
        candidate["forecast"] = {"ok": 0, "calls": []}  # old forecasts never follow revised wording
        state["candidates"] = [candidate]
        state["selected"] = 0
        state["events"].append({"step": "revision", "text": data["text"], "at": utcnow(), "origin": "user_reply_in_chat"})
        _review(project, state, model)
    elif action == "accept":
        _accept(project, state, data)
    else:
        raise PreparationNeeded("I'll use the current coaching step before continuing.")
    _save(project, state)
    return packet(state)


def cmd_coach(a):
    project = Path(a.project).resolve()
    if getattr(a, "check", False):
        ok, why = fg.accepted(project)
        print(("ACCEPTED: " if ok else "NOT YET: ") + why)
        return 0 if ok else 2
    try:
        data = read_json(Path(a.response_file)) if getattr(a, "response_file", None) else None
        model = fg.model_for(project) if getattr(a, "model_review", False) else None
        result = act(project, getattr(a, "action", "status"), data, model,
                     getattr(a, "header", None), getattr(a, "axis", None), getattr(a, "name", None))
        code = 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, StopIteration) as error:
        result = {"status": "needs_preparation", "message": str(error) if isinstance(error, PreparationNeeded) else
                  "I couldn't read the saved coaching information. I'll check it before asking you to continue.",
                  "for_the_assistant": getattr(error, "detail", "Check the response/session files and use the current revision."),
                  "can_accept": False}
        code = 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code
