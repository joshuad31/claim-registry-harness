"""Byte limits, Unicode fidelity, provenance and conversion retry integration."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scratch import scratch_dir, cleanup
from claimreg.corpus_intake import MAX_SOURCE_BYTES, MIN_SPLIT_BYTES, split_bytes, admit_bytes, part_map, logical_count
from claimreg.corpus import ingest, Corpus
from claimreg import cli
import test_conversion as fixtures
response = fixtures.response


class IntakeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir('intake')
        self.root = self.tmp / '01_CORPUS/source-files'
        self.root.mkdir(parents=True)

    def tearDown(self):
        cleanup(self.tmp)

    def test_exact_boundary_and_utf8_are_lossless(self):
        for data in (b'x' * MAX_SOURCE_BYTES, b'x' * (MAX_SOURCE_BYTES + 1),
                     ('# Hebrew\n\n' + 'דְּרוֹר 自由 🕊️\n' * 20000).encode(),
                     ('א' * 220000).encode()):
            with self.subTest(size=len(data)):
                paths = admit_bytes(self.root, 'paper.md', data)
                self.assertEqual(b''.join(p.read_bytes() for p in paths), data)
                self.assertTrue(all(p.stat().st_size <= MAX_SOURCE_BYTES for p in paths))
                for p in paths:
                    p.read_bytes().decode('utf-8')
                self.assertEqual(logical_count(self.root, paths), 1)
                if len(paths) > 1:
                    entry = part_map(self.root)[paths[0].relative_to(self.root).as_posix()]
                    self.assertEqual(Path(entry['original_archive']).read_bytes(), data)
                    self.assertFalse(Path(entry['original_archive']).is_relative_to(self.root))

    def test_external_drop_is_preserved_and_replaced_before_manifest(self):
        original = b'# Findings\n\n' + b'quote exactly\n' * 40000
        (self.root / 'paper.md').write_bytes(original)
        man = ingest(self.tmp, self.root)
        self.assertGreater(man['files'], 1)
        self.assertEqual(man['logical_sources'], 1)
        self.assertFalse((self.root / 'paper.md').exists())
        self.assertEqual(len({s['logical_source_id'] for s in man['sources']}), 1)
        self.assertTrue(all(s['bytes'] <= MAX_SOURCE_BYTES for s in man['sources']))
        self.assertEqual(man['manifest_id'], ingest(self.tmp, self.root)['manifest_id'])

    def test_split_documents_never_leave_tiny_pieces(self):
        for size in (210001, 223105, 229999, 230000, 250000, 420001, 629999, 630001):
            for unit in (b'x', b'paragraph\n\n', 'דְּרוֹר 🕊️\n'.encode()):
                # Repeat complete Unicode units; exercise unbroken and structured text.
                data = unit * (size // len(unit) + 1)
                with self.subTest(size=len(data), unit=unit):
                    parts = split_bytes(data)
                    self.assertEqual(b''.join(parts), data)
                    self.assertTrue(all(MIN_SPLIT_BYTES <= len(p) <= MAX_SOURCE_BYTES for p in parts))
                    for part in parts:
                        part.decode('utf-8')
        self.assertEqual([len(p) for p in split_bytes(b'x' * 223105)], [111552, 111553])

    def test_naturally_small_documents_are_not_padded(self):
        for data in (b'', b'short document', b'x' * 19999):
            self.assertEqual(split_bytes(data), [data])

    def test_collisions_and_edited_parts_are_preserved(self):
        paths = admit_bytes(self.root, 'paper.md', b'x' * 420001)
        paths[0].write_text('User correction', encoding='utf-8')
        with self.assertRaises(ValueError):
            admit_bytes(self.root, 'paper.md', b'x' * 420001)
        self.assertEqual(paths[0].read_text(), 'User correction')

    def test_legacy_encoding_original_is_preserved(self):
        data = b'caf\xe9\n' * 50000
        paths = admit_bytes(self.root, 'legacy.md', data)
        self.assertEqual(b''.join(p.read_bytes() for p in paths).decode('utf-8'), data.decode('cp1252'))
        entry = next(iter(part_map(self.root).values()))
        self.assertEqual(Path(entry['original_archive']).read_bytes(), data)

    def test_bom_removal_can_produce_one_piece_without_leaving_oversized_original(self):
        data = b'\xef\xbb\xbf' + b'x' * (MAX_SOURCE_BYTES - 1)
        (self.root / 'bom.md').write_bytes(data)
        man = ingest(self.tmp, self.root)
        self.assertEqual(man['files'], 1)
        self.assertFalse((self.root / 'bom.md').exists())
        self.assertLessEqual(man['sources'][0]['bytes'], MAX_SOURCE_BYTES)
        self.assertEqual(Path(man['sources'][0]['split_origin']['original_archive']).read_bytes(), data)

    def test_study_identity_and_original_filename_exclusions_survive(self):
        from types import SimpleNamespace
        from claimreg import studies, frd_assess
        data = b'# Critical review\n\n' + b'Literature discussion\n' * 24000
        paths = admit_bytes(self.root, 'reference.md', data)
        corpus = Corpus(ingest(self.tmp, self.root))
        cfg = {'corpus': {'synthesis_sources': ['reference.md']}}
        smap = studies.build_map(self.tmp, corpus, cfg)
        self.assertEqual(len(smap['studies']), 1)
        self.assertTrue(all(r['kind'] == 'synthesis' for r in smap['files'].values()))
        row = {'frd_id': 'F1', 'source_file': paths[1].name}
        ctx = SimpleNamespace(corpus=corpus, cfg=cfg)
        self.assertEqual(frd_assess.citable(ctx, [row])[0], [])
        self.assertTrue(frd_assess.is_synthesis(ctx, paths[1].name))
        ctx.cfg = {'corpus': {'duplicates': {'reference.md': 'canonical.md'}}}
        self.assertEqual(frd_assess.citable(ctx, [row])[0], [])

    def test_cli_add_and_stale_manifest_guard(self):
        source = self.tmp / 'staged.md'
        source.write_bytes(b'x' * 420001)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(['init', str(self.tmp)]), 0)
            self.assertEqual(cli.main(['corpus', str(self.tmp), '--add', str(source)]), 0)
        self.assertTrue(source.exists())
        man = ingest(self.tmp, self.root)
        (self.root / man['sources'][0]['filename']).write_bytes(b'x' * 210001)
        with self.assertRaisesRegex(ValueError, '210,000'):
            Corpus(man)


class SplitConversionTest(unittest.TestCase):
    setUp = fixtures.ConversionTest.setUp
    tearDown = fixtures.ConversionTest.tearDown
    run_conversion = fixtures.ConversionTest.run_conversion
    def test_large_conversion_is_split_and_retry_does_not_upload(self):
        self.session.get.return_value = response({'status': 'complete', 'markdown': 'א' * 220000})
        self.assertEqual(self.run_conversion()[0]['status'], 'converted')
        parts = sorted(self.out.glob('*.md'))
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(p.stat().st_size <= MAX_SOURCE_BYTES for p in parts))
        self.assertEqual(b''.join(p.read_bytes() for p in parts).decode(), 'א' * 220000 + '\n')
        self.session.reset_mock()
        self.assertEqual(self.run_conversion()[0]['status'], 'skipped')
        self.session.post.assert_not_called()
        parts[0].write_text('edited')
        self.assertEqual(self.run_conversion()[0]['status'], 'existing_unverified')
        self.session.post.assert_not_called()


if __name__ == '__main__':
    unittest.main()
