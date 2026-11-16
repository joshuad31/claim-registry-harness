"""Advisory startup host detection. No profile edits, installation, or network calls."""
from __future__ import annotations

import json
import os
from pathlib import Path
from zipfile import is_zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name("deepseek-preset.json")
PRESET_ID = "claim-registry"


def _preset_release(manifest_path=None, root=None):
    root = Path(root) if root is not None else ROOT
    try:
        data = json.loads(Path(manifest_path or MANIFEST).read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("status") != "ready":
            return {"status": "pending", "bundle_path": None}
        if data.get("preset_id") != PRESET_ID:
            raise ValueError("Unexpected preset identity")
        path = data.get("bundle_path")
        if not isinstance(path, str) or not path.strip() or Path(path).is_absolute():
            raise ValueError("A bundled release needs a relative archive path")
        bundle = (root / path).resolve()
        if not bundle.is_relative_to(root.resolve()) or not bundle.is_file() or not is_zipfile(bundle):
            raise ValueError("No valid bundled archive")
        return {"status": "ready", "bundle_path": str(bundle)}
    except (OSError, ValueError, TypeError):
        # Presence of a sibling dist ZIP is deliberately not a release signal.
        return {"status": "unavailable", "bundle_path": None}


def check_host(environ=None, active_preset=None, manifest_path=None, root=None):
    env = os.environ if environ is None else environ
    # These are documented per-execution facts supplied by DSH's shell-env service.
    # DSH_HOME alone, an installed application, and a DeepSeek model/key are insufficient.
    detected = env.get("DSH_SHELL") == "1" and bool(str(env.get("DSH_SESSION_ID") or "").strip())
    release = _preset_release(manifest_path, root)
    result = {"host": "deepseek-harness" if detected else "unknown",
              "evidence": ["DSH_SHELL", "DSH_SESSION_ID"] if detected else [],
              "active_preset": active_preset, "preset_id": PRESET_ID, "release": release,
              "action": "none", "message": "", "advisory_only": True,
              "for_the_assistant": "Use this as a host hint, not a security check. Do not infer the app from the model name, "
                                   "an installed package, or DSH_PROFILE (a profile is not a selected preset). "
                                   "Pass --active-preset only from visible session metadata or an explicit user confirmation. "
                                   "Never install a pending/unavailable bundle or redirect a working session repeatedly. "
                                   "The regular research workflow can continue here."}
    if not detected:
        return result
    if active_preset == PRESET_ID:
        result["action"] = "already_using_preset"
    elif release["status"] == "ready":
        result.update(action="suggest_preset_session",
                      message="For the best DeepSeek Harness setup, install the included Claim Registry preset, "
                              "then start a new session with Claim Registry selected. We can also continue here.")
    else:
        result.update(action="preset_pending",
                      message="A Claim Registry preset for DeepSeek Harness is being finalized. Once it is available, "
                              "install it and start a new session with Claim Registry selected; for now we can continue here.")
    return result


def startup_notice(active_preset=None):
    result = check_host(active_preset=active_preset)
    # Keep non-DSH startup unchanged. No process scans, credential reads, or user-name guessing.
    if result["host"] != "deepseek-harness":
        return ""
    return ("HOST CHECK (for the assistant):\n" + json.dumps(result, ensure_ascii=False, indent=2) +
            "\nIf there is a message, offer it briefly alongside the opening question. Do not ask the user to "
            "install the DeepSeek application again. Skip the notice if session metadata confirms the preset is already active.\n\n")


def cmd_host(a):
    print(json.dumps(check_host(active_preset=getattr(a, "active_preset", None)), ensure_ascii=False, indent=2))
    return 0
