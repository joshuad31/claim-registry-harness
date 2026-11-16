"""Lossless, byte-limited corpus admission; originals live outside the corpus."""
from __future__ import annotations

import hashlib
import json
import os
import threading
import uuid
from pathlib import Path

MAX_SOURCE_BYTES = 210_000
MIN_SPLIT_BYTES = 20_000
EXTENSIONS = {'.md', '.markdown', '.txt'}
_LOCK = threading.RLock()


def _atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.' + uuid.uuid4().hex + '.pending')
    try:
        tmp.write_bytes(data)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def part_map(root):
    path = Path(root) / '.corpus-parts.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def split_bytes(data):
    """Prefer paragraph/line/word boundaries; never cut a UTF-8 character."""
    data.decode('utf-8')  # caller normalizes legacy encodings before splitting
    parts = []
    while len(data) > MAX_SOURCE_BYTES:
        end = MAX_SOURCE_BYTES
        while True:
            try:
                data[:end].decode('utf-8')
                break
            except UnicodeDecodeError:
                end -= 1
        for boundary in (b'\n\n', b'\n', b' '):
            pos = data.rfind(boundary, end // 2, end)
            if pos >= 0:
                end = pos + len(boundary)
                break
        parts.append(data[:end])
        data = data[end:]
    parts.append(data)
    if len(parts) > 1 and len(parts[-1]) < MIN_SPLIT_BYTES:
        combined = parts[-2] + parts[-1]
        if len(combined) <= MAX_SOURCE_BYTES:
            parts[-2:] = [combined]
        else:
            # Redistribute the final pair, preserving text and useful boundaries.
            midpoint = len(combined) // 2
            lower = max(MIN_SPLIT_BYTES, len(combined) - MAX_SOURCE_BYTES)
            upper = min(MAX_SOURCE_BYTES, len(combined) - MIN_SPLIT_BYTES)
            cut = midpoint
            for boundary in (b'\n\n', b'\n', b' '):
                positions = (combined.rfind(boundary, lower, midpoint + 1),
                             combined.find(boundary, midpoint, upper))
                candidates = [p + len(boundary) for p in positions
                              if p >= 0 and lower <= p + len(boundary) <= upper]
                if candidates:
                    cut = min(candidates, key=lambda p: abs(p - midpoint))
                    break
            while combined[cut] & 0xC0 == 0x80:
                cut -= 1
            parts[-2:] = [combined[:cut], combined[cut:]]
    return parts


def admit_bytes(root, relative, data):
    """Return actual admitted paths. Safe to retry; refuse conflicting part names."""
    root = Path(root).resolve()
    relative = Path(relative)
    dest = (root / relative).resolve()
    if not dest.is_relative_to(root) or dest == root:
        raise ValueError('Corpus destination must be inside the source folder')
    with _LOCK:
        mapping = part_map(root)
        original = hashlib.sha256(data).hexdigest()
        if len(data) <= MAX_SOURCE_BYTES:
            payloads = [data]
            paths = [dest]
        else:
            try:
                text = data.decode('utf-8-sig')
            except UnicodeDecodeError:
                text = data.decode('cp1252')
            payloads = split_bytes(text.encode('utf-8'))
            paths = [dest.with_name(f'{dest.stem}--{original[:12]}.part-{n:04d}{dest.suffix}')
                     for n in range(1, len(payloads) + 1)]
            for path, body in zip(paths, payloads):
                if path.exists() and path.read_bytes() != body:
                    raise ValueError(f'Corpus part already exists with different content: {path.name}')
            corpus_parent = next((p for p in root.parents if p.name == '01_CORPUS'), None)
            archive_root = (corpus_parent.parent / '99_ARCHIVE' / 'corpus-originals'
                            if corpus_parent else root.parent / (root.name + '-originals'))
            archive = archive_root / (original + dest.suffix)
            if archive.exists() and archive.read_bytes() != data:
                raise ValueError('Original archive conflicts with its content hash')
            _atomic(archive, data)
        old = [name for name, entry in mapping.items() if entry['original_filename'] == relative.as_posix()]
        for name in old:
            path = root / name
            if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != mapping[name]['part_sha256']:
                raise ValueError(f'Edited corpus part must be reconciled before replacement: {name}')
        for path, body in zip(paths, payloads):
            _atomic(path, body)
        for name in old:
            if root / name not in paths:
                (root / name).unlink(missing_ok=True)
            del mapping[name]
        if len(data) > MAX_SOURCE_BYTES:
            offset = 0
            for n, (path, body) in enumerate(zip(paths, payloads), 1):
                mapping[path.relative_to(root).as_posix()] = {
                    'original_filename': relative.as_posix(), 'original_sha256': original,
                    'logical_source_id': 'SRC-' + original[:12],
                    'part': n, 'parts': len(paths), 'utf8_start': offset,
                    'utf8_end': offset + len(body),
                    'part_sha256': hashlib.sha256(body).hexdigest(),
                    'original_archive': str(archive),
                }
                offset += len(body)
        if mapping or old:
            _atomic(root / '.corpus-parts.json', (json.dumps(mapping, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
        if len(data) > MAX_SOURCE_BYTES:
            # Remove a manual drop only after the original, parts and provenance are saved.
            dest.unlink(missing_ok=True)
        return paths


def admit_file(root, source, relative=None):
    source = Path(source)
    return admit_bytes(root, relative or source.name, source.read_bytes())


def normalize_corpus(root):
    root = Path(root)
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.suffix.lower() in EXTENSIONS and path.stat().st_size > MAX_SOURCE_BYTES:
            admit_file(root, path, path.relative_to(root))


def logical_count(root, files):
    mapping = part_map(root)
    return len({mapping.get(p.relative_to(root).as_posix(), {}).get('logical_source_id', p.relative_to(root).as_posix())
                for p in files})
