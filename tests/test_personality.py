"""Default startup and Cursor must carry every supplied file without lossy summaries."""
import contextlib
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from claimreg import cli, personality
from scratch import scratch_dir, cleanup
from tools.package_research_kit import build, write_cursor_rules


class PersonalityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("personality")

    def tearDown(self):
        cleanup(self.tmp)

    def capture(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cli.main(list(args))
        return code, out.getvalue()

    def test_all_eleven_original_files_are_preserved_byte_for_byte(self):
        manifest = json.loads((personality.PACKAGE / "INTEGRATION.json").read_text())
        self.assertEqual(len(manifest["files"]), 11)
        self.assertEqual(sum(row["path"].startswith("memory/") for row in manifest["files"]), 6)
        for row in manifest["files"]:
            data = (personality.PACKAGE / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_start_and_reload_contain_every_complete_file_not_just_links(self):
        for args in ((), ("start",), ("launch",), ("personality",)):
            code, text = self.capture(*args)
            self.assertEqual(code, 0)
            for name, path in personality.source_files():
                self.assertIn(f"COMPLETE PACKAGE FILE: {name}", text)
                self.assertIn(path.read_text(encoding="utf-8-sig"), text)

    def test_small_parts_reconstruct_the_entire_payload(self):
        chunks = personality.parts()
        self.assertGreater(len(chunks), 1)
        self.assertEqual("".join(chunks), personality.render())
        for i, chunk in enumerate(chunks, 1):
            code, text = self.capture("personality", "--part", str(i))
            self.assertEqual(code, 0)
            self.assertEqual(text.split("\n", 1)[1], chunk)
            self.assertLessEqual(len(chunk), personality.PART_CHARS)
        self.assertEqual(self.capture("personality", "--part", "0")[0], 2)

    def test_missing_memory_prevents_apparently_successful_startup(self):
        package = self.tmp / "package"
        package.mkdir()
        (package / "PERSONALITY.md").write_text("Fixture profile")
        (package / "INTEGRATION.json").write_text(json.dumps({"files": [{"path": "missing.md"}]}))
        with patch.object(personality, "PACKAGE", package), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.capture("start")[0], 2)

    def test_new_memory_is_included_without_changing_an_allowlist(self):
        package = self.tmp / "package"
        package.mkdir()
        (package / "PERSONALITY.md").write_text("Fixture profile")
        (package / "INTEGRATION.json").write_text('{"files": []}')
        (package / "new-lesson.md").write_text("New learned workflow")
        self.assertIn("New learned workflow", personality.render(package))

    def test_cursor_rules_are_always_on_and_inline_every_file(self):
        outputs = write_cursor_rules(self.tmp / "rules")
        bodies = [p.read_text(encoding="utf-8") for p in outputs]
        self.assertEqual(len(outputs), len(personality.source_files()) + 1)
        for text in bodies:
            self.assertIn("alwaysApply: true", text.split("---", 2)[1])
        for name, path in personality.source_files():
            self.assertTrue(any(f"Complete source file: {name}\n" in s and
                                path.read_text(encoding="utf-8-sig") in s for s in bodies))

    def test_rebuilt_archive_keeps_every_imported_file(self):
        with ZipFile(build(self.tmp / "personality.zip")) as z:
            for name, path in personality.source_files():
                self.assertEqual(z.read("research-paper-converter/" + name), path.read_bytes())


if __name__ == "__main__":
    unittest.main()
