"""Acceptance gate for the LEVO bedtime-dosing assessment.  Not a scorer.

Adapted from the reference gate written with the audit (ChatGPT, 2026-11-11).  It checks the
assessor's DECLARED evidence uses against a small audited catalog of trial protocols.  It cannot
tell whether the assessor described its own reasoning faithfully: a person still reads the drivers.

One change from the reference gate: a driver whose source is not in the catalog is accepted as
indirect or background evidence (with a transfer argument), and rejected only if it is declared a
direct test of the target.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# NOTE (2026-11-11, pre-run audit): the harness actually runs `bedtime_gate_v2.check`, which the
# harness feeds the frozen frame, every `allocation_drivers` entry with its real FRD source file,
# the non-citable synthesis list and the duplicate map; v2 enforces R16-R21 on top of this gate.
# This v1 module keeps the audited source catalog, the base CONTRACT and the 16 fixture cases.

CONTRACT = """GATE REPORT (required for this axis). After the allocation JSON block append one more fenced JSON block:
{"gate_report": {
 "frame": {"comparison_type": "practical_strategy | optimized_schedules | clock_time | decision_to_offer",
           "target_bedtime_min_gap_minutes": 180, "target_morning_min_gap_minutes": 60,
           "target_population": "persistent_high_tsh_boundary | broad_adults",
           "success_logic": "any | all", "accepted_outcomes": ["tsh_target", "ft4", "symptoms"]},
 "exposure_ledger": {"morning": [{"factor": "", "status": ""}], "bedtime": [{"factor": "", "status": ""}]},
 "drivers": [{"source_id": "bolk_2010 | bach_huynh_2009 | de_mello_2022 | <other source>", "frd_id": "",
              "direction": "favors_bedtime | against_bedtime | neither",
              "inference_type": "direct_target_estimate | direct_target_refutation | indirect | background",
              "transfer_justification": ""}],
 "causal_uses": [{"mechanism": "", "caused_by_schedule": true, "direction": "benefit | harm", "interpretation": "benefit_mechanism | refute_h1 | erase_effect | not_used"}],
 "alternative_uses": [{"alternative_could_work": true, "conclusion": "alternative_option_only | bedtime_has_no_benefit"}],
 "endpoint_uses": [{"endpoint": "", "result": "null | positive | negative", "conclusion_scope": "this_endpoint_only | whole_h1"}],
 "equivalence_uses": [{"claim": "equivalent | not_claimed", "basis": "nonsignificant_difference | equivalence_design"}],
 "ppi_resolved_by_clock_separation": false,
 "population_weighting": {"numerical_population_effect_claimed": false, "joint_prevalence_measured": false},
 "scored_gap_ids": ["<each unresolved gap once>"],
 "exclude_repaired_claim_only_because_legacy_wrong": false,
 "weighting_method": "holistic_study_and_comparison_assessment | count_frds"}}
Declare what you actually did. A report that declares a prohibited use is returned for correction; it is not scored."""

SOURCES = {
    "bolk_2010": {"morning_gap_minutes": 30, "bedtime_gap_minutes": None,
        "matches_persistent_high_tsh_boundary": False,
        "url": "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/776486"},
    "bach_huynh_2009": {"morning_gap_minutes": 60, "bedtime_gap_minutes": 120,
        "matches_persistent_high_tsh_boundary": False,
        "url": "https://pubmed.ncbi.nlm.nih.gov/19584184/"},
    "de_mello_2022": {"morning_gap_minutes": 60, "bedtime_gap_minutes": 60,
        "matches_persistent_high_tsh_boundary": False,
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9261378/"},
}


def check(report):
    errors = []

    def fail(rule, message):
        errors.append({"rule": rule, "message": message})

    if not isinstance(report, dict):
        return [{"rule": "CONTRACT", "message": "No gate report was supplied"}]
    required_report = ("frame", "allocations", "exposure_ledger", "drivers", "causal_uses", "alternative_uses",
        "endpoint_uses", "equivalence_uses", "ppi_resolved_by_clock_separation", "population_weighting",
        "scored_gap_ids", "exclude_repaired_claim_only_because_legacy_wrong", "weighting_method")
    if any(k not in report for k in required_report):
        return [{"rule": "CONTRACT", "message": "Required checks cannot be omitted"}]
    frame = report.get("frame", {})
    required = ("comparison_type", "target_bedtime_min_gap_minutes", "target_morning_min_gap_minutes",
        "target_population", "success_logic", "accepted_outcomes", "hypothesis_ids", "gauge")
    if any(k not in frame for k in required):
        fail("R1", "Missing explicit frame fields")
        return errors
    if frame["comparison_type"] not in ("practical_strategy", "optimized_schedules", "clock_time", "decision_to_offer"):
        fail("R1", "Unknown comparison type")
    if frame["gauge"] != 64:
        fail("ARITHMETIC", "This reference gate requires G=64")
    vec = report.get("allocations", {})
    if (set(vec) != set(frame["hypothesis_ids"]) or
        any(type(v) is not int or v < 0 for v in vec.values()) or sum(vec.values()) != 64):
        fail("ARITHMETIC", "Allocations need exact IDs and nonnegative integers summing to 64")
    exposures = report.get("exposure_ledger", {})
    if not exposures.get("morning") or not exposures.get("bedtime"):
        fail("R7", "Both schedule exposure ledgers are required")

    for d in report.get("drivers", []):
        facts = SOURCES.get(d.get("source_id"))
        inference = d.get("inference_type")
        if inference not in ("direct_target_estimate", "direct_target_refutation", "indirect", "background"):
            fail("R9", "Specify direct, indirect or background use")
            continue
        if not facts:
            if inference.startswith("direct_target"):
                fail("R4", f"{d.get('source_id')} is not in the audited protocol catalog, so it cannot be declared a "
                           f"direct test of the target; add its protocol to the catalog after source review")
            elif inference == "indirect" and not str(d.get("transfer_justification", "")).strip():
                fail("R9", "Indirect evidence requires an explicit transfer argument and limitation")
            continue
        if inference.startswith("direct_target"):
            gap = facts["bedtime_gap_minutes"]
            if gap is None or gap < frame["target_bedtime_min_gap_minutes"]:
                fail("R4", f"{d['source_id']} does not directly test the target bedtime food gap")
            if frame["comparison_type"] in ("optimized_schedules", "clock_time"):
                gap = facts["morning_gap_minutes"]
                if gap is None or gap < frame["target_morning_min_gap_minutes"]:
                    fail("R4", f"{d['source_id']} does not directly test the target morning food gap")
            if frame["target_population"] == "persistent_high_tsh_boundary" and not facts["matches_persistent_high_tsh_boundary"]:
                fail("R9", f"{d['source_id']} is not a direct boundary-matched refractory estimate")
        elif inference == "indirect" and not d.get("transfer_justification", "").strip():
            fail("R9", "Indirect evidence requires an explicit transfer argument and limitation")

    for c in report.get("causal_uses", []):
        # R2 forbids erasing a schedule-caused BENEFIT (better adherence/less interference). A
        # schedule-caused HARM (e.g. nocturnal contamination reducing absorption) may legitimately
        # be declared "harm" and used against H1; that is evidence, not an adjustment.
        if (c.get("caused_by_schedule") and c.get("direction", "benefit") != "harm"
                and c.get("interpretation") in ("refute_h1", "erase_effect")):
            fail("R2", "A schedule-caused adherence or exposure improvement cannot erase its total effect")
    for a in report.get("alternative_uses", []):
        if a.get("alternative_could_work") and a.get("conclusion") == "bedtime_has_no_benefit":
            fail("R3", "An alternative remedy does not logically disprove benefit from the switch")
    for e in report.get("endpoint_uses", []):
        if (frame["success_logic"] == "any" and len(frame["accepted_outcomes"]) > 1 and
            e.get("result") == "null" and e.get("conclusion_scope") == "whole_h1" and
            not e.get("covers_all_accepted_endpoints", False)):
            fail("R10", "A null result on one endpoint cannot refute the entire OR-defined H1")
    for e in report.get("equivalence_uses", []):
        if e.get("claim") == "equivalent" and e.get("basis") == "nonsignificant_difference":
            fail("R11", "Nonsignificance alone does not establish equivalence")
    if report.get("ppi_resolved_by_clock_separation") is True:
        fail("R6", "Clock separation alone does not establish resolution of persistent PPI acid suppression")
    w = report.get("population_weighting", {})
    if w.get("numerical_population_effect_claimed") and not w.get("joint_prevalence_measured"):
        fail("R8", "A numerical population effect needs supported joint exposure weights; assumptions need separate scenario status")
    gaps = report.get("scored_gap_ids", [])
    if len(gaps) != len(set(gaps)):
        fail("R12", "A repeated gap cannot be scored as separate independent adverse findings")
    if report.get("exclude_repaired_claim_only_because_legacy_wrong"):
        fail("R13", "The current repaired claim must be judged using its retained support")
    if report.get("weighting_method") == "count_frds":
        fail("R14", "Counting FRDs is not independent-study weighting")
    return errors


def merge(base, patch):
    result = copy.deepcopy(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result


def self_test():
    fixtures = json.loads((HERE / "gate_examples.json").read_text(encoding="utf-8"))
    rows = []
    for case in fixtures["cases"]:
        errors = check(merge(fixtures["base_report"], case["patch"]))
        actual_rules = sorted({e["rule"] for e in errors})
        expected_rules = sorted(case.get("expected_rules", []))
        passed = (not errors) == case["expect_accept"] and actual_rules == expected_rules
        rows.append({"case": case["name"], "test_passed": passed,
            "report_accepted": not errors, "expected_accept": case["expect_accept"], "rules": actual_rules})
    result = {"synthetic_tests_not_scientific_allocations": True,
        "tests": len(rows), "passed": sum(r["test_passed"] for r in rows), "cases": rows,
        "limits": "Checks declared fields against three source protocols; semantic completeness still requires review."}
    return result
