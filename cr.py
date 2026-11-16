#!/usr/bin/env python3
"""Claim Registry harness launcher:  python cr.py <command> ...   (`python cr.py start` if you were asked to launch it)"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
