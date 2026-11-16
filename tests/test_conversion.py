"""Conversion contract tests: no live network, credentials, or paid requests."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from claimreg import cli, conversion
from scratch import scratch_dir, cleanup
from tools.package_research_kit import build, FILES


def response(data, code=200):
    r = Mock(status_code=code)
    r.json.return_value = data
    return r


class ConversionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("conversion")
        self.src = self.tmp / "pdf"
        self.src.mkdir()
        self.paper = self.src / "article.pdf"
        self.paper.write_bytes(b"%PDF-1.4 synthetic fixture")
        self.out = self.tmp / "text"
        self.key = self.tmp / "external-key"
        self.key.write_text("fixture-secret-do-not-log")
        self.session = Mock()
        self.session.post.return_value = response({"request_check_url": conversion.ENDPOINT + "/job1"})
        self.session.get.return_value = response({"status": "complete", "success": True,
                                                "markdown": "# Finding\nValue < 5; dose 2 mg.", "page_count": 1})

    def tearDown(self):
        cleanup(self.tmp)

    def run_conversion(self, **kw):
        return conversion.convert_folder(self.src, self.out, key_file=self.key,
                                         factory=lambda: self.session, sleep=lambda _: None, **kw)

    def test_preview_has_no_upload_key_requirement_or_output(self):
        result = conversion.convert_folder(self.src, self.out, dry_run=True,
                                            factory=lambda: self.fail("network during preview"))
        self.assertEqual(result[0]["status"], "planned")
        self.assertFalse(self.out.exists())

    def test_text_is_clean_and_only_matching_outputs_skip(self):
        self.assertEqual(self.run_conversion()[0]["status"], "converted")
        dest = self.out / "article.pdf.md"
        self.assertEqual(dest.read_text(), "# Finding\nValue < 5; dose 2 mg.\n")
        self.session.reset_mock()
        self.assertEqual(self.run_conversion()[0]["status"], "skipped")
        self.session.post.assert_not_called()
        self.paper.write_bytes(b"%PDF-1.4 changed source")
        self.assertEqual(self.run_conversion()[0]["status"], "existing_unverified")
        self.session.post.assert_not_called()
        self.assertNotIn(self.key.read_text(), "".join(p.read_text() for p in self.out.rglob("*.json")))

    def test_nested_same_names_are_not_overwritten(self):
        (self.src / "topic").mkdir()
        (self.src / "topic" / "article.pdf").write_bytes(b"%PDF other")
        self.assertEqual([r["status"] for r in self.run_conversion()], ["converted", "converted"])
        self.assertTrue((self.out / "topic" / "article.pdf.md").exists())

    def test_pending_job_resumes_without_another_post(self):
        self.session.get.return_value = response({"status": "processing"})
        self.assertEqual(self.run_conversion(polls=1)[0]["status"], "failed")
        self.session.reset_mock()
        self.session.get.return_value = response({"status": "complete", "success": True, "markdown": "Result"})
        self.assertEqual(self.run_conversion()[0]["status"], "converted")
        self.session.post.assert_not_called()

    def test_unknown_submission_is_not_automatically_billed_again(self):
        self.session.post.side_effect = TimeoutError("fixture-secret-do-not-log")
        first = self.run_conversion()
        self.assertNotIn(self.key.read_text(), json.dumps(first))
        self.session.reset_mock()
        self.assertEqual(self.run_conversion()[0]["status"], "failed")
        self.session.post.assert_not_called()

    def test_credentials_never_follow_untrusted_poll_urls(self):
        self.session.post.return_value = response({"request_check_url": "https://example.org/capture"})
        self.assertEqual(self.run_conversion()[0]["status"], "failed")
        self.session.get.assert_not_called()

    def test_empty_and_failed_remote_results_do_not_create_evidence(self):
        for result in ({"status": "complete", "success": True, "markdown": " "},
                       {"status": "failed", "success": False}):
            self.session.get.return_value = response(result)
            self.assertEqual(self.run_conversion(force=True)[0]["status"], "failed")
            self.assertFalse((self.out / "article.pdf.md").exists())

    def test_project_cli_uses_configured_source_directory_without_ingestion(self):
        project = self.tmp / "project"
        project.mkdir()
        (project / "project.json").write_text(json.dumps({"corpus": {"source_dir": "custom-text"}}))
        with patch("claimreg.conversion.convert_folder", return_value=[]) as call, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["convert", str(project), "--folder", str(self.src), "--dry-run"]), 0)
        self.assertEqual(call.call_args.args[1], project / "custom-text")
        self.assertFalse((project / "01_CORPUS" / "manifests").exists())

    def test_portable_zip_has_only_allowlisted_content_and_neutral_metadata(self):
        path = build(self.tmp / "kit.zip")
        with ZipFile(path) as z:
            self.assertEqual(len(z.infolist()), len(FILES))
            for i in z.infolist():
                self.assertEqual(i.date_time, (2026, 11, 15, 0, 0, 0))
                self.assertFalse(i.comment or i.extra)
                self.assertNotIn("older-versions/", i.filename)
                self.assertNotIn(b"fixture-secret-do-not-log", z.read(i))
            # Restored research experience is part of the distribution, not discarded on rebuild.
            from claimreg.personality import source_files
            for name, source in source_files():
                self.assertEqual(z.read("research-paper-converter/" + name), source.read_bytes())


if __name__ == "__main__":
    unittest.main()
