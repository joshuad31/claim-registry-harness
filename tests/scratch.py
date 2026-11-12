"""A scratch directory that works in confined Windows sandboxes.

``tempfile.mkdtemp`` creates a directory the sandbox token cannot write inside
on some Windows setups (a restrictive ACL is applied to the 0o700 directory).
A plainly created, uniquely named directory under the checkout works
everywhere.  Set ``CR_TEST_TMP`` to move it.
"""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def scratch_dir(tag: str = "crtest") -> Path:
    base = Path(os.environ.get("CR_TEST_TMP") or (_ROOT / ".tmp"))
    base.mkdir(parents=True, exist_ok=True)
    d = base / f"{tag}-{uuid.uuid4().hex[:10]}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


# The researcher's stop after the preliminary FRD evaluation is on by default.  The pipeline tests
# were written to run straight through, so it is off for the suite; tests/test_frd_assess.py turns
# it back on to test it.
import sys as _sys  # noqa: E402

_sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from claimreg import config as _config  # noqa: E402

_config.DEFAULT_CONFIG["pipeline"]["stop_after"] = ""

# The frame gate keeps its signer and its lock in the user's home folder.  The suite must neither
# read the real ones nor be stopped by a locked gate, so both point into the scratch area here.
from claimreg import frame_gate as _frame_gate  # noqa: E402

_gate_home = Path(os.environ.get("CR_TEST_TMP") or (_ROOT / ".tmp")) / "frame-gate-home"
_frame_gate.SIGNER_FILE = _gate_home / "signer.json"
_frame_gate.LOCK_FILE = _gate_home / "FRAME-GATE-LOCKED"
