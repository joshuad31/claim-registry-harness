"""Detect the host conservatively; unfinished preset packages are never offered as ready."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from claimreg import cli, checklist, personality, host_context as hc
from scratch import scratch_dir, cleanup

DSH_ENV = {"DSH_SHELL": "1", "DSH_SESSION_ID": "test-session-not-for-display"}


class HostContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("host-context")
        self.manifest = self.tmp / "preset.json"
        self.write_manifest("pending")

    def tearDown(self):
        cleanup(self.tmp)

    def write_manifest(self, state, bundle=None):
        self.manifest.write_text(json.dumps({"status": state, "preset_id": hc.PRESET_ID, "bundle_path": bundle}))

    def check(self, env=DSH_ENV, **kwargs):
        return hc.check_host(env, manifest_path=self.manifest, root=self.tmp, **kwargs)

    def ready_bundle(self):
        archive = self.tmp / "resources" / "preset.zip"
        archive.parent.mkdir()
        with ZipFile(archive, "w") as z:
            z.writestr("package.json", '{"name":"test-preset"}')
        self.write_manifest("ready", "resources/preset.zip")

    def test_dsh_requires_actual_shell_session_markers(self):
        self.assertEqual(self.check()["host"], "deepseek-harness")
        for env in ({}, {"DSH_HOME": "installed"}, {"DSH_SHELL": "1"},
                    {"DSH_SESSION_ID": "session"}, {"DSH_SHELL": "1", "DSH_SESSION_ID": None},
                    {"DSH_SHELL": "1", "DSH_SESSION_ID": " "},
                    {"MODEL": "deepseek-chat", "DEEPSEEK_API_KEY": "fixture-no-real-key"}):
            with self.subTest(env=list(env)):
                result = self.check(env)
                self.assertEqual(result["host"], "unknown")
                self.assertFalse(result["message"])
                self.assertEqual(result["action"], "none")

    def test_unfinished_zip_presence_does_not_enable_installation_recommendation(self):
        self.ready_bundle()
        self.write_manifest("pending", "resources/preset.zip")
        result = self.check()
        self.assertEqual(result["action"], "preset_pending")
        self.assertEqual(result["release"], {"status": "pending", "bundle_path": None})
        self.assertTrue(result["advisory_only"])
        self.assertNotIn("test-session-not-for-display", json.dumps(result))

    def test_ready_release_recommends_installation_and_a_new_preset_session(self):
        self.ready_bundle()
        result = self.check()
        self.assertEqual(result["action"], "suggest_preset_session")
        self.assertTrue(Path(result["release"]["bundle_path"]).is_file())
        self.assertIn("new session", result["message"])
        self.assertIn("Claim Registry selected", result["message"])

    def test_already_selected_preset_does_not_get_another_setup_prompt(self):
        for ready in (False, True):
            if ready:
                self.ready_bundle()
            result = self.check(active_preset="claim-registry")
            self.assertEqual(result["action"], "already_using_preset")
            self.assertFalse(result["message"])

    def test_profile_name_is_not_selected_preset_evidence(self):
        self.ready_bundle()
        result = self.check({**DSH_ENV, "DSH_PROFILE": "claim-registry"})
        self.assertEqual(result["action"], "suggest_preset_session")
        self.assertIsNone(result["active_preset"])

    def test_missing_invalid_or_external_ready_archive_cannot_be_recommended(self):
        for name in ("missing.zip", "broken.zip", "../outside.zip", str(self.tmp / "absolute.zip")):
            with self.subTest(path=name):
                (self.tmp / "broken.zip").write_text("not an archive")
                self.write_manifest("ready", name)
                result = self.check()
                self.assertEqual(result["release"]["status"], "unavailable")
                self.assertNotEqual(result["action"], "suggest_preset_session")

    def test_bad_release_metadata_does_not_stop_normal_startup(self):
        self.manifest.write_text("invalid JSON")
        self.assertEqual(self.check()["action"], "preset_pending")

    def test_all_startup_entry_points_include_the_check_and_complete_personality(self):
        for args in ([], ["start"], ["launch"]):
            with self.subTest(args=args), patch.dict(hc.os.environ, DSH_ENV, clear=True), \
                    patch.object(hc, "MANIFEST", self.manifest), contextlib.redirect_stdout(io.StringIO()) as out:
                code = cli.main(args)
                text = out.getvalue()
                self.assertEqual(code, 0)
                self.assertTrue(text.startswith(checklist.START_TEXT))
                self.assertIn('"action": "preset_pending"', text)
                self.assertIn(personality.render(), text)

    def test_host_command_checks_without_installing_or_starting_research(self):
        with patch.dict(hc.os.environ, DSH_ENV, clear=True), contextlib.redirect_stdout(io.StringIO()) as out:
            code = cli.main(["host", "--active-preset", "claim-registry"])
        self.assertEqual(code, 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result["action"], "already_using_preset")
        self.assertFalse(result["message"])


if __name__ == "__main__":
    unittest.main()
