import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scratch import scratch_dir, cleanup
from claimreg.json_files import json_folder, organize


class JsonFilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir('json-files')

    def tearDown(self):
        cleanup(self.tmp)

    def test_threshold_and_two_fixed_path_exceptions(self):
        for name in ('coaching-session.json', 'frame-certificate.json'):
            (self.tmp / name).write_text('{}')
        self.assertEqual(organize(self.tmp), [])
        (self.tmp / 'reply.json').write_text('{"text":"actual reply"}')
        keep = ('coaching-session.json', 'frame-certificate.json')
        plan = organize(self.tmp, keep, dry_run=True)
        self.assertEqual(len(plan), 1)
        self.assertFalse((self.tmp / 'json').exists())
        organize(self.tmp, keep)
        self.assertEqual((self.tmp / 'json/reply.json').read_text(), '{"text":"actual reply"}')
        self.assertTrue(all((self.tmp / n).exists() for n in keep))
        self.assertEqual(organize(self.tmp, keep), [])

    def test_reuses_existing_case_and_never_nests(self):
        folder = self.tmp / 'JSON'
        folder.mkdir()
        self.assertEqual(json_folder(self.tmp), folder)
        for n in range(3):
            (folder / f'{n}.json').write_text('{}')
        self.assertEqual(organize(folder), [])
        self.assertFalse((folder / 'json').exists())

    def test_different_collision_prevents_any_move(self):
        folder = self.tmp / 'json'
        folder.mkdir()
        for n in range(3):
            (self.tmp / f'{n}.json').write_text(str(n))
        (folder / '2.json').write_text('different')
        with self.assertRaises(ValueError):
            organize(self.tmp)
        self.assertEqual(len(list(self.tmp.glob('*.json'))), 3)
        self.assertEqual((folder / '2.json').read_text(), 'different')
