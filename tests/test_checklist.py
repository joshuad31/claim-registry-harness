"""`cr next`: the checklist a person sees on the way to a first quest.

Progress is read from the project's files, so any assistant that asks gets the same answer.  It
never claims more than the files show, it asks no model anything, and it is not a gate.
"""

import contextlib
import io
import json
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg import checklist, cli  # noqa: E402
from claimreg.llm.router import LLM  # noqa: E402
from claimreg.onramp import QUESTION_TEMPLATE  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_pipeline_mock import make_project  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
QUESTION = """# The question

## What I want to decide

Does a foliar silicate spray raise wheat yield under drought?

## Who or what it is about (scope)

Field-grown wheat under water stress; not greenhouse trials.

## The competing answers (hypotheses)

1. The spray raises yield under drought.
2. Any gain comes from the extra water in the spray, not the silicate.
3. The evidence cannot yet tell 1 from 2.

## What evidence would tell them apart

A field trial with a water-only spray as the comparison.
"""


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = cli.main(list(argv))
    return code, out.getvalue()


def by_id(st):
    return {i["id"]: i for i in st["items"]}


class ChecklistTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("checklist")
        self.proj = self.tmp / "Wheat"
        code, _ = run("new", str(self.proj), "--name", "Silicate and wheat")
        self.assertEqual(code, 0)

    def tearDown(self):
        cleanup(self.tmp)

    def test_before_there_is_a_project_the_first_step_is_the_question(self):
        st = checklist.build(None)
        self.assertEqual((st["project"], st["next"]["id"], st["steps"]), (None, "question", 9))
        self.assertIn("What do you want to research?", st["next"]["for_the_assistant"])
        code, text = run("next")
        self.assertEqual(code, 0)
        self.assertIn("Next: Say what you want to research", text)
        self.assertIn("Why:", text)
        # a folder that is not a project yet reads the same way, and cannot be confirmed into
        self.assertEqual(run("next", str(self.tmp / "nothing"))[1].count("Next: Say what you want"), 1)
        self.assertEqual(run("next", str(self.tmp / "nothing"), "--done", "sources")[0], 2)

    def test_each_step_follows_the_files(self):
        it = by_id(checklist.build(self.proj))
        self.assertEqual((it["question"]["progress"], it["hypotheses"]["progress"]), (0, 0))   # the untouched template
        q = self.proj / "01_FRAME" / "question.md"
        self.assertEqual(q.read_text(encoding="utf-8"), QUESTION_TEMPLATE)
        # the question and its scope, nothing else yet
        half = QUESTION.split("## The competing answers")[0] + QUESTION_TEMPLATE[QUESTION_TEMPLATE.index("## The competing"):]
        q.write_text(half, encoding="utf-8")
        st = checklist.build(self.proj)
        it = by_id(st)
        self.assertEqual((it["question"]["state"], it["hypotheses"]["progress"], st["next"]["id"]), ("done", 0, "hypotheses"))
        # two rivals but not what would tell them apart
        q.write_text(QUESTION.split("## What evidence")[0] + "## What evidence would tell them apart\n\nREPLACE: later\n",
                     encoding="utf-8")
        it = by_id(checklist.build(self.proj))
        self.assertEqual((it["hypotheses"]["progress"], it["hypotheses"]["missing"]),
                         (67, ["what evidence would tell them apart"]))
        q.write_text(QUESTION, encoding="utf-8")
        st = checklist.build(self.proj)
        self.assertEqual((by_id(st)["hypotheses"]["state"], st["next"]["id"]), ("done", "sources"))

    def test_sources_count_pdfs_and_wait_for_the_persons_word(self):
        (self.proj / "01_FRAME" / "question.md").write_text(QUESTION, encoding="utf-8")
        pdf = self.proj / "01_CORPUS" / "pdf"
        pdf.mkdir(parents=True)
        (pdf / "okafor2019.pdf").write_bytes(b"%PDF")
        (pdf / "li2024.pdf").write_bytes(b"%PDF")
        src = ROOT / "examples" / "demo" / "sources" / "okafor2019.md"
        (self.proj / "01_CORPUS" / "source-files" / "okafor2019.md").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        it = by_id(checklist.build(self.proj))
        self.assertEqual(it["sources"]["progress"], 50)                       # files exist; completeness not confirmed
        self.assertIn("2 sources collected", it["sources"]["detail"])          # one converted, one PDF still waiting
        self.assertIn("1 PDF waiting", it["convert"]["detail"])
        self.assertIn("is your own confirmation", it["sources"]["basis"])
        # only what files cannot show can be confirmed by hand
        self.assertEqual(run("next", str(self.proj), "--done", "frame")[0], 2)
        self.assertEqual(run("next", str(self.proj), "--done", "sources")[0], 0)
        self.assertEqual(by_id(checklist.build(self.proj))["sources"]["state"], "done")
        self.assertEqual(json.loads((self.proj / "CHECKLIST.json").read_text())["confirmed"].keys(), {"sources"})
        run("next", str(self.proj), "--undo", "sources")
        self.assertEqual(by_id(checklist.build(self.proj))["sources"]["progress"], 50)
        # converting the second file and registering the sources completes the conversion step
        (pdf / "li2024.pdf").unlink()
        self.assertEqual(run("corpus", str(self.proj))[0], 0)
        self.assertEqual(by_id(checklist.build(self.proj))["convert"]["state"], "done")

    def test_search_notes_beside_the_corpus_are_not_sources(self):
        notes = self.proj / "01_CORPUS" / "search-notes.md"
        notes.write_text("queries I ran", encoding="utf-8")
        self.assertIn("none yet", by_id(checklist.build(self.proj))["sources"]["detail"])

    def test_frame_notebook_and_launch(self):
        cfg = json.loads((self.proj / "project.json").read_text())
        cfg["coach"] = {"require_acceptance": True}                           # the product default; the suite turns it off
        (self.proj / "project.json").write_text(json.dumps(cfg))
        st0 = by_id(checklist.build(self.proj))
        self.assertEqual((st0["frame"]["progress"], st0["notebook"]["progress"], st0["launch"]["progress"]), (0, 0, 0))
        hdr = (ROOT / "tests" / "fixtures" / "mini" / "header.md").read_text(encoding="utf-8")
        (self.proj / "01_FRAME" / "header-DRAFT.md").write_text(hdr, encoding="utf-8")
        it = by_id(checklist.build(self.proj))
        self.assertEqual((it["frame"]["progress"], it["frame"]["detail"]), (33, "draft written; not yet approved"))
        self.assertEqual(it["hypotheses"]["state"], "done")                    # a drafted header implies them
        self.assertEqual(run("approve", str(self.proj), "--by", "A Researcher")[0], 0)
        it = by_id(checklist.build(self.proj))
        self.assertEqual((it["frame"]["progress"], it["frame"]["missing"]), (67, ["the session with the coach"]))
        self.assertIn("Do not answer it for them", it["frame"]["for_the_assistant"])
        # notebook: a link, then the person's word about the settings
        cfg = json.loads((self.proj / "project.json").read_text())
        cfg["notebooklm"] = {"notebooks": ["https://notebooklm.google.com/notebook/3b728d29-628f-4c3e-9b0d-ce485d37d24a"]}
        (self.proj / "project.json").write_text(json.dumps(cfg))
        it = by_id(checklist.build(self.proj))
        self.assertEqual(it["notebook"]["progress"], 50)
        self.assertIn("3 to 6 copies are recommended", it["notebook"]["detail"])
        run("next", str(self.proj), "--done", "notebook")
        self.assertEqual(by_id(checklist.build(self.proj))["notebook"]["state"], "done")
        # a started quest is the last step, and what comes after is named
        (self.proj / "quest" / "Q1").mkdir(parents=True)
        (self.proj / "quest" / "Q1" / "quest.json").write_text("{}")
        st = checklist.build(self.proj)
        self.assertEqual((by_id(st)["launch"]["state"], st["launched"]), ("done", True))

    def test_a_project_that_already_ran_is_not_asked_to_confirm_the_past(self):
        proj = make_project(self.tmp)
        from claimreg.pipeline import run_pipeline
        from claimreg.runctx import RunContext
        self.assertEqual(run_pipeline(RunContext(proj, "RUN-C", create=True, quiet=True), stop="quest")["status"], "complete")
        st = checklist.build(proj)
        it = by_id(st)
        self.assertEqual([it[k]["state"] for k in ("sources", "notebook", "launch")], ["done", "done", "done"])
        self.assertEqual(st["next"]["id"], "after-launch")

    def test_outputs_and_the_window(self):
        (self.proj / "01_FRAME" / "question.md").write_text(QUESTION, encoding="utf-8")
        code, js = run("next", str(self.proj), "--json")
        st = json.loads(js)
        self.assertEqual(set(st["next"]) >= {"title", "why", "do", "for_the_assistant", "guide"}, True)
        self.assertTrue(all((ROOT / i["guide"]).exists() for i in st["items"]))
        md = run("next", str(self.proj), "--md")[1]
        self.assertIn("| 3 | Collect your sources |", md)
        self.assertIn("**next**", md)
        text = run("next", str(self.proj))[1]
        self.assertLessEqual(len(text.splitlines()), 20)                        # never a wall of text
        self.assertTrue(text.isascii())                                         # safe in any console
        # no page until someone asks for the window; afterwards every `cr next` keeps it current
        self.assertFalse((self.proj / "CHECKLIST.html").exists())
        page = checklist.write_page(self.proj)
        html = page.read_text(encoding="utf-8")
        self.assertIn("Next step", html)
        self.assertEqual(html.count("<details"), len(checklist.GUIDE_PAGES))
        self.assertNotIn("<script src", html)                                   # self-contained
        run("next", str(self.proj), "--done", "sources")
        self.assertNotEqual(page.read_text(encoding="utf-8"), html)

    def test_it_asks_no_model_and_contacts_nothing(self):
        calls = []
        orig = (LLM.call, LLM.call_many)
        LLM.call = lambda *a, **k: calls.append(a)
        LLM.call_many = lambda *a, **k: calls.append(a)
        try:
            checklist.build(self.proj)
            checklist.write_page(self.proj)
        finally:
            LLM.call, LLM.call_many = orig
        self.assertEqual(calls, [])


class GuideTest(unittest.TestCase):
    def test_pages_are_short_and_render(self):
        for page in checklist.GUIDE_PAGES:
            text = (checklist.GUIDE_DIR / f"{page}.md").read_text(encoding="utf-8")
            self.assertLessEqual(len(text.split()), 230, page)                 # about a minute to read
            self.assertNotIn("|---", text, page)                               # the window does not render tables
            title, body = checklist.md_to_html(text)
            self.assertTrue(title and "<p>" in body, page)
            self.assertNotIn("**", body, page)
            for tag in ("ul", "ol", "p"):
                self.assertEqual(body.count(f"<{tag}>"), body.count(f"</{tag}>"), (page, tag))
        index = (checklist.GUIDE_DIR / "README.md").read_text(encoding="utf-8")
        self.assertTrue(all(f"({p}.md)" in index for p in checklist.GUIDE_PAGES))

    def test_the_guide_never_points_at_a_pirate_library(self):
        text = " ".join(f.read_text(encoding="utf-8").lower() for f in checklist.GUIDE_DIR.glob("*.md"))
        text += (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
        for name in ("sci-hub", "scihub", "libgen", "library genesis", "z-library", "anna's archive"):
            self.assertNotIn(name, text)

    def test_launching_reaches_the_opening_question_from_any_door(self):
        # Every launch entry point includes both the opening and the complete research personality.
        outs = [run(*argv) for argv in ([], ["start"], ["launch"])]
        self.assertTrue(all(code == 0 for code, _ in outs))
        self.assertEqual(len({text for _, text in outs}), 1)
        text = outs[0][1]
        self.assertIn("What do you want to research?", text)
        self.assertIn("Do not run the tests or the demo", text)
        from claimreg import personality
        self.assertTrue(text.startswith(checklist.START_TEXT))
        self.assertIn(personality.render(), text)
        for f in ("START HERE.md", "README.md", "AGENTS.md"):
            head = "\n".join((ROOT / f).read_text(encoding="utf-8").splitlines()[:16])
            self.assertIn("python cr.py start", head, f)
        self.assertLessEqual(len((ROOT / "START HERE.md").read_text(encoding="utf-8").split()), 160)
        self.assertTrue((ROOT / "docs" / "BUILD-RECORD.md").exists())

    def test_the_assistant_file_separates_the_two_jobs_and_sets_the_opening(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertLess(text.index("HANDOFF.md"), text.index("What do you want to research?"))
        self.assertIn("python cr.py next", text)
        self.assertLessEqual(len(text.split()), 1700)
        for f in ("CLAUDE.md", "GEMINI.md"):
            self.assertIn("AGENTS.md", (ROOT / f).read_text(encoding="utf-8"))

    def test_the_assistant_is_told_to_mentor_and_to_help_with_papers(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        start = checklist.START_TEXT
        # the second reply leads with the person's question and the value, not with a list of limits
        self.assertLess(agents.index("Take the question seriously"), agents.index("Mention a limit only if"))
        self.assertIn("Never open with what it cannot do", agents)
        self.assertIn("Never open with what it cannot do", start)
        self.assertNotIn("do not sell", agents.lower())
        # papers: the assistant does the legwork, and a failed download comes with its reason
        self.assertIn("say exactly why", agents)
        self.assertIn("say exactly why", start)
        st = checklist.build(None)
        self.assertEqual(by_id(st)["sources"]["guide"], "docs/guide/getting-papers.md")
        page = (checklist.GUIDE_DIR / "what-it-does.md").read_text(encoding="utf-8")
        self.assertNotIn("find sources for you", page)

    def test_the_developer_handoff_does_not_capture_a_lost_assistant(self):
        # HANDOFF.md is 50 KB of build record.  An assistant that opens it first must still be
        # sent to the opening question before it is told to read this file.
        text = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:12])
        self.assertIn("python cr.py start", head)
        self.assertIn("There is no program to launch", head)
        self.assertLess(head.index("python cr.py start"), head.index("read this file first"))


if __name__ == "__main__":
    unittest.main()
