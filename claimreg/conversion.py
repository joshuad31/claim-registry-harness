"""Optional Datalab conversion; also runnable as a standalone folder converter.

Only selected documents leave the machine. Credentials are never written to records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

ENDPOINT = "https://www.datalab.to/api/v1/convert"
EXTENSIONS = {".pdf", ".doc", ".docx", ".pptx", ".epub"}
MODES = ("accurate", "balanced", "fast")


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def save(path, record):
    write(path, json.dumps(record, indent=2, ensure_ascii=False) + "\n")


def check_url(url):
    p = urlsplit(url)
    if (p.scheme != "https" or p.hostname != "www.datalab.to" or p.port not in (None, 443)
            or p.username or p.password or not p.path.startswith("/api/v1/convert/")):
        raise ValueError("Unexpected conversion result URL; credentials were not sent to it")
    return url


def checked(response):
    # Never include response bodies or exception strings: either may echo a secret.
    if response.status_code != 200:
        raise ValueError(f"Datalab HTTP {response.status_code}")
    result = response.json()
    if not isinstance(result, dict):
        raise ValueError("Invalid Datalab JSON response")
    return result


def convert_one(source, relative, output, key, mode, force, factory, sleep=time.sleep, polls=360):
    dest = output / (relative.as_posix() + ".md")
    state_path = output / ".conversion-state" / (hashlib.sha256(relative.as_posix().encode()).hexdigest() + ".json")
    record = {}
    try:
        if state_path.exists():
            record = json.loads(state_path.read_text(encoding="utf-8"))
        fingerprint = sha(source)
        same = record.get("source_sha256") == fingerprint and record.get("mode") == mode
        if dest.exists() and not force:
            verified = (same and record.get("status") == "complete" and dest.stat().st_size > 0
                        and record.get("output_sha256") == sha(dest))
            return {"source": relative.as_posix(), "status": "skipped" if verified else "existing_unverified"}
        session = factory()
        try:
            headers = {"X-API-Key": key}
            if same and record.get("request_check_url") and record.get("status") == "pending" and not force:
                url = check_url(record["request_check_url"])
            else:
                if same and record.get("status") == "submitting" and not force:
                    return {"source": relative.as_posix(), "status": "failed",
                            "reason": "Previous submission outcome unknown; inspect provider jobs before --force"}
                record = {"source": relative.as_posix(), "source_sha256": fingerprint,
                          "mode": mode, "status": "submitting"}
                save(state_path, record)
                with source.open("rb") as f:
                    response = session.post(ENDPOINT, headers=headers, files={"file": (source.name, f)},
                                            data={"mode": mode, "output_format": "markdown"},
                                            timeout=300, allow_redirects=False)
                job = checked(response)
                url = check_url(job["request_check_url"])
                record.update(status="pending", request_check_url=url)
                save(state_path, record)
            for _ in range(polls):
                response = session.get(url, headers=headers, timeout=60, allow_redirects=False)
                if response.status_code == 429:
                    sleep(30)
                    continue
                result = checked(response)
                if result.get("status") == "failed" or result.get("success") is False:
                    record["status"] = "failed"
                    save(state_path, record)
                    raise ValueError("Datalab reported conversion failure")
                if result.get("status") == "complete":
                    md = result.get("markdown")
                    if not isinstance(md, str) or not md.strip():
                        raise ValueError("Conversion completed without nonempty Markdown")
                    if sha(source) != fingerprint:
                        raise ValueError("Source changed during conversion; output not written")
                    # Keep the document clean; provenance belongs in its JSON sidecar.
                    write(dest, md.rstrip() + "\n")
                    record.update(status="complete", output_sha256=sha(dest), pages=result.get("page_count"))
                    save(state_path, record)
                    return {"source": relative.as_posix(), "status": "converted", "pages": record["pages"]}
                sleep(5)
            raise ValueError("Polling limit reached; run again to resume this job without resubmitting")
        finally:
            session.close()
    except Exception as e:
        allowed = ("Datalab HTTP ", "Datalab reported ", "Conversion completed ", "Source changed ",
                   "Polling limit ", "Unexpected conversion ", "Invalid Datalab ")
        reason = str(e) if isinstance(e, ValueError) and str(e).startswith(allowed) else type(e).__name__
        return {"source": relative.as_posix(), "status": "failed", "reason": reason}


def convert_folder(folder, output=None, mode="accurate", key_file=None, dry_run=False, force=False,
                   workers=3, factory=None, sleep=time.sleep, polls=360):
    folder = Path(folder).resolve()
    output = Path(output).resolve() if output else folder / "Markdowns"
    if not folder.is_dir():
        raise ValueError("Input folder does not exist")
    if mode not in MODES or not 1 <= workers <= 8:
        raise ValueError("Invalid conversion mode or worker count")
    files = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS
                   and not p.is_symlink())
    if dry_run:
        return [{"source": p.relative_to(folder).as_posix(), "status": "planned",
                 "output": str(output / (p.relative_to(folder).as_posix() + ".md"))} for p in files]
    if not files:
        return []
    key = Path(key_file).read_text(encoding="utf-8-sig").strip() if key_file else os.environ.get("DATALAB_API_KEY", "").strip()
    if not key:
        raise ValueError("Set DATALAB_API_KEY or supply --key-file (never paste a key into chat)")
    if factory is None:
        try:
            import requests
        except ImportError:
            raise ValueError("Optional dependency missing: install requests") from None
        factory = requests.Session
    def one(p):
        return convert_one(p, p.relative_to(folder), output, key, mode, force, factory, sleep, polls)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(one, files))


def cmd_convert(a):
    from .config import load_config, resolve_path
    project = Path(a.project)
    if not (project / "project.json").is_file():
        print("convert: open or create a Claim Registry project first")
        return 2
    cfg = load_config(project)
    try:
        records = convert_folder(a.folder or project / "01_CORPUS" / "pdf",
                                 resolve_path(cfg, cfg["corpus"]["source_dir"]), a.mode,
                                 a.key_file, a.dry_run, a.force, a.workers)
        print(json.dumps(records, indent=2, ensure_ascii=False))
        if records and not a.dry_run:
            print("Review extraction fidelity, then run cr corpus to register the reviewed text. No automatic ingestion.")
        return 2 if any(r["status"] in ("failed", "existing_unverified") for r in records) else 0
    except (ValueError, OSError) as e:
        print("convert: " + (str(e) if isinstance(e, ValueError) else type(e).__name__))
        return 2


def main():
    p = argparse.ArgumentParser(description="Convert local papers with Datalab (external, potentially paid upload)")
    p.add_argument("folder")
    p.add_argument("--output")
    p.add_argument("--mode", choices=MODES, default="accurate")
    p.add_argument("--key-file")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--workers", type=int, default=3)
    a = p.parse_args()
    try:
        result = convert_folder(a.folder, a.output, a.mode, a.key_file, a.dry_run, a.force, a.workers)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2 if any(r["status"] in ("failed", "existing_unverified") for r in result) else 0
    except (ValueError, OSError) as e:
        print(str(e) if isinstance(e, ValueError) else type(e).__name__)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
