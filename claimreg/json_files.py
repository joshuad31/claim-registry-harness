"""Keep assistant-created JSON payloads out of human-facing folders.

Engine files with fixed contract paths must be explicitly retained by the caller.
"""
from pathlib import Path


def json_folder(directory):
    directory = Path(directory)
    existing = [p for p in directory.iterdir() if p.name.lower() == 'json'] if directory.exists() else []
    if len(existing) > 1 or (existing and not existing[0].is_dir()):
        raise ValueError('Resolve the conflicting json folder names before organizing files')
    return existing[0] if existing else directory / 'json'


def organization_plan(directory, keep=()):
    directory = Path(directory).resolve()
    if directory.name.lower() == 'json':
        return []  # never create json/json
    keep = {name.lower() for name in keep}
    if len(keep) > 2:
        raise ValueError('At most two JSON files may remain outside the json folder')
    files = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == '.json')
    if len(files) <= 2:
        return []
    target = json_folder(directory)
    plan = []
    for source in files:
        if source.name.lower() in keep:
            continue
        if source.is_symlink():
            raise ValueError('JSON symlinks require explicit reconciliation')
        dest = target / source.name
        if dest.exists() and (not dest.is_file() or dest.read_bytes() != source.read_bytes()):
            raise ValueError(f'Different files share the destination name: {source.name}')
        plan.append((source, dest))
    return plan


def organize(directory, keep=(), dry_run=False):
    plan = organization_plan(directory, keep)
    if dry_run:
        return plan
    for source, dest in plan:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            if source.read_bytes() != dest.read_bytes():
                raise ValueError(f'Destination changed: {source.name}')
            source.unlink()  # identical copy already preserved in json
        else:
            source.rename(dest)
    return plan
