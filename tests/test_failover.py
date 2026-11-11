"""Per-role provider failover in the router: mechanical triggers, provenance, cache, single-provider behaviour."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fakes  # noqa: E402
from claimreg.config import load_config  # noqa: E402
from claimreg.llm import router as router_mod  # noqa: E402
from claimreg.llm.base import LLMRequest, LLMResponse, ProviderError  # noqa: E402
from claimreg.llm.router import LLM  # noqa: E402
from claimreg.util import read_jsonl, write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402


def good(req, prov):
    return {"ok": True, "from": prov.name}


class FailoverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("failover")
        fakes.reset()
        self._sleep = router_mod.backoff_sleep
        router_mod.backoff_sleep = lambda attempt: None

    def tearDown(self):
        router_mod.backoff_sleep = self._sleep
        cleanup(self.tmp)

    def llm(self, roles, scripts):
        fakes.SCRIPTS.update(scripts)
        write_json(self.tmp / "project.json", {
            "roles": roles,
            "providers": {n: {"type": "scripted", "model": f"model-{n}", "script": n} for n in scripts},
            "budget": {"retries": 1, "concurrency": 2}})
        return LLM(load_config(self.tmp))

    def req(self, user="hello"):
        return LLMRequest(role="frd_validator", system="s", user=user, tag="t1")

    def test_single_provider_string_still_works(self):
        llm = self.llm({"frd_validator": "a"}, {"a": good})
        r = llm.call(self.req())
        self.assertEqual(r.parsed["from"], "a")
        self.assertEqual(r.failover, [])

    def test_content_filter_finish_moves_to_next_provider(self):
        def filtered(req, prov):
            return LLMResponse(text="", finish_reason="content_filter")
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": filtered, "b": good})
        r = llm.call(self.req())
        self.assertEqual(r.provider, "b")
        self.assertEqual(r.failover[0]["provider"], "a")
        self.assertIn("content_filter", r.failover[0]["reason"])
        self.assertEqual(llm.failovers, 1)
        rows = read_jsonl(llm.log_path)
        self.assertEqual([x["status"] for x in rows], ["failover", "ok"])
        self.assertEqual(rows[1]["failover"][0]["provider"], "a")

    def test_refusal_text_with_normal_finish_is_not_matched_in_prose(self):
        # a hedged but valid JSON answer must never be treated as a refusal
        def hedged(req, prov):
            return {"answer": "I cannot be certain, but the source says X."}
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": hedged, "b": good})
        self.assertEqual(llm.call(self.req()).provider, "a")

    def test_http_400_policy_body_moves_on_without_retry(self):
        def blocked(req, prov):
            raise fakes.http_error(400, '{"error": {"code": "content_policy_violation"}}')
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": blocked, "b": good})
        r = llm.call(self.req())
        self.assertEqual(r.provider, "b")
        self.assertIn("content filter", r.failover[0]["reason"])
        self.assertEqual([c[0] for c in fakes.CALLS], ["a", "b"])

    def test_timeout_is_retried_then_moves_on(self):
        def down(req, prov):
            raise fakes.http_error(0, "timed out")
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": down, "b": good})
        r = llm.call(self.req())
        self.assertEqual(r.provider, "b")
        self.assertEqual([c[0] for c in fakes.CALLS], ["a", "a", "b"])   # one retry (budget.retries = 1)

    def test_bad_json_twice_moves_on(self):
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": lambda req, prov: "not json at all", "b": good})
        r = llm.call(self.req())
        self.assertEqual(r.provider, "b")
        self.assertIn("JSON", r.failover[0]["reason"])

    def test_all_fail_raises_once_through_the_list(self):
        def blocked(req, prov):
            raise fakes.http_error(403, "blocked by safety system")
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": blocked, "b": blocked})
        with self.assertRaises(ProviderError) as cm:
            llm.call(self.req())
        self.assertIn("earlier providers skipped", str(cm.exception))
        self.assertEqual([c[0] for c in fakes.CALLS], ["a", "b"])        # one pass, no loop

    def test_answer_from_second_provider_is_cached_for_the_role(self):
        def filtered(req, prov):
            return LLMResponse(text="", finish_reason="refusal")
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": filtered, "b": good})
        llm.call(self.req())
        n = len(fakes.CALLS)
        again = llm.call(self.req())
        self.assertTrue(again.cached)
        self.assertEqual(again.provider, "b")
        self.assertEqual(len(fakes.CALLS), n)

    def test_provider_with_no_credits_is_asked_once_then_skipped(self):
        def broke(req, prov):
            raise fakes.http_error(429, '{"error": {"type": "insufficient_quota", "message": "You have no credits remaining."}}')
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": broke, "b": good})
        rs = llm.call_many([self.req(f"q{i}") for i in range(6)])
        self.assertTrue(all(r.provider == "b" for r in rs))
        self.assertIn("a", llm.down)
        self.assertLessEqual(sum(1 for c in fakes.CALLS if c[0] == "a"), 2)     # no retries, no repeat visits
        later = llm.call(self.req("another"))
        self.assertIn("skipped for this run", later.failover[0]["reason"])
        self.assertIn("providers_down", llm.usage_summary())

    def test_empty_answer_at_the_length_limit_gets_one_larger_budget(self):
        seen = []

        def thinker(req, prov):
            seen.append(req.max_output_tokens)
            if req.max_output_tokens is None:
                return LLMResponse(text="", finish_reason="length")
            return {"ok": True, "from": prov.name}
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": thinker, "b": good})
        r = llm.call(self.req())
        self.assertEqual(r.provider, "a")
        self.assertEqual(seen, [None, 32000])

    def test_a_cut_off_answer_is_asked_for_again_when_the_request_says_it_must_be_whole(self):
        import dataclasses
        seen = []

        def cut_off(req, prov):
            seen.append(req.max_output_tokens)
            if len(seen) == 1:
                return LLMResponse(text='{"ok": tr', finish_reason="length")
            return {"ok": True, "from": prov.name}
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": cut_off, "b": good})
        r = llm.call(dataclasses.replace(self.req(), meta={"retry_if_truncated": True}))
        self.assertEqual(r.provider, "a")
        self.assertEqual(len(seen), 2)
        self.assertGreaterEqual(seen[1], 32000)

    def test_call_many_survives_one_provider_refusing_everything(self):
        def filtered(req, prov):
            return LLMResponse(text="", finish_reason="content_filter")
        llm = self.llm({"frd_validator": ["a", "b"]}, {"a": filtered, "b": good})
        rs = llm.call_many([self.req(f"q{i}") for i in range(5)])
        self.assertTrue(all(r.provider == "b" for r in rs))
        self.assertEqual(llm.error_count, 0)


if __name__ == "__main__":
    unittest.main()
