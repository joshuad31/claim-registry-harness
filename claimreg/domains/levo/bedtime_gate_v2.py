"""DRAFT (Grok Bot audit, 2026-11-11), not installed. Hardened acceptance gate for the LEVO bedtime axis.

What changes from bedtime_gate.py (v1):
  * The harness, not the model, supplies the facts that matter: the frozen frame (from module options /
    the approved header), each allocation driver's source file (from the FRD registry), and the list of
    synthesis (non-citable) sources.  A model can no longer dodge a check by declaring
    target_population "broad_adults" or by leaving a list empty.
  * Every driver in the ALLOCATION block must be declared in the gate report with the same direction,
    so the declaration can't differ from what moved the vector (this let an A2 replay pass in v1).
  * Drivers quoting an AI synthesis, or a duplicate copy, are rejected as drivers.
  * A driver favouring H2/H3 that comes from a catalogued trial whose bedtime food gap is below the
    target must be declared indirect, with a bridge that names the gap.
  * The exposure ledger must cover a fixed list of factors on BOTH schedules, each with a status.
  * Required safety block and stratified (exposure-profile) conclusions.
It still cannot read the model's mind: a person must read the drivers against their sources.
"""
from __future__ import annotations
import copy
from . import bedtime_gate as v1

# Audited protocol catalog (extends v1).  Values taken from the abstracts verified 2026-11-11; the
# bedtime gaps for Bolk 2010 / Skelin / Rajput must be filled from the full text before use as DIRECT.
SOURCES = {**v1.SOURCES,
  "bolk_2007": {"files": ["bolk2006.pdf.md"], "morning_gap_minutes": None, "bedtime_gap_minutes": None,
                "matches_persistent_high_tsh_boundary": False, "pmid": "17201800"},
  "skelin_2018": {"files": ["skelin2018.pdf.md"], "morning_gap_minutes": None, "bedtime_gap_minutes": None,
                  "matches_persistent_high_tsh_boundary": False, "pmid": "30043093"},
  "rajput_2011": {"files": ["rajput2011.pdf.md"], "morning_gap_minutes": None, "bedtime_gap_minutes": None,
                  "matches_persistent_high_tsh_boundary": False, "pmid": "21785690"},
  "perez_2013": {"files": ["perez2013.pdf.md"], "morning_gap_minutes": 30, "bedtime_gap_minutes": None,
                 "matches_persistent_high_tsh_boundary": False, "pmid": "23363386"},
  "pang_2020": {"files": ["pang2020.pdf.md"], "morning_gap_minutes": None, "bedtime_gap_minutes": None,
                "matches_persistent_high_tsh_boundary": False, "pmid": "32022947", "pooled": True},
}
FILE_TO_SOURCE = {"bolk2010.pdf.md": "bolk_2010", "bach-huynh2009.pdf.md": "bach_huynh_2009",
                  "fmed-09-828762.pdf.md": "de_mello_2022"}
for sid, f in SOURCES.items():
    for fn in f.get("files", []):
        FILE_TO_SOURCE[fn] = sid

LEDGER_FACTORS = ("breakfast_gap", "coffee", "calcium_or_dairy", "iron", "multivitamin", "ppi_or_h2ra",
                  "other_binders", "evening_meal_or_snack_gap", "missed_doses", "shift_or_irregular_sleep",
                  "gi_disease_celiac_hpylori_atrophic_gastritis", "tsh_sampling_time")
LEDGER_STATUS = ("measured", "reported", "inferred", "unknown")
STRATA = ("documented_removable_morning_interference", "persistent_non_timing_cause", "no_documented_interference")
SAFETY = ("overreplacement_recheck_weeks", "bedtime_interferents_checked", "sampling_time_standardised",
          "no_dose_change_at_switch", "high_risk_groups_named")
GAP_WORDS = ("gap", "hour", "min", "interval")


def check(report: dict | None, ctx: dict) -> list[dict]:
    """ctx is built by the harness: {"frame": <frozen frame>, "allocation_drivers": [{frd_id, favors,
    source_file}], "synthesis_sources": [...], "duplicates": {copy: original}, "h1_id": "A2-H1"}."""
    errors = []
    fail = lambda r, m: errors.append({"rule": r, "message": m})
    if not isinstance(report, dict):
        return [{"rule": "CONTRACT", "message": "No gate report was supplied"}]
    rep = copy.deepcopy(report)
    rep["frame"] = {**(rep.get("frame") or {}), **ctx["frame"]}          # frozen frame wins over declaration
    errors += v1.check(rep)

    declared = {(d.get("frd_id") or "").strip(): d for d in rep.get("drivers", [])}
    syn = set(ctx.get("synthesis_sources", []))
    dup = ctx.get("duplicates", {})
    h1 = ctx.get("h1_id", "A2-H1")
    if len(ctx.get("allocation_drivers", [])) < int(ctx.get("min_drivers", 3)):
        fail("R17", "fewer than the minimum number of allocation drivers; an allocation must say what moved it")
    for fid in ctx.get("unknown_driver_ids", []):
        fail("R17", f"driver {fid} is not an FRD in this axis's registry")
    for a in ctx.get("allocation_drivers", []):
        fid, fav, sf = a["frd_id"], a.get("favors", ""), a.get("source_file", "")
        if sf in syn:
            fail("R16", f"{fid} quotes the synthesis document '{sf}'; a synthesis is a lead, never a driver")
        if sf in dup:
            fail("R14", f"{fid} quotes a duplicate copy '{sf}' of '{dup[sf]}'; cite the original once")
        d = declared.get(fid)
        if d is None:
            fail("R17", f"allocation driver {fid} is not declared in the gate report")
            continue
        want = "favors_bedtime" if fav == h1 else "against_bedtime"
        if d.get("direction") not in (want, "neither"):
            fail("R17", f"{fid}: gate-report direction '{d.get('direction')}' does not match the allocation ({fav})")
        sid = FILE_TO_SOURCE.get(sf)
        facts = SOURCES.get(sid) if sid else None
        if fav != h1 and facts is not None:
            gap = facts.get("bedtime_gap_minutes")
            if gap is not None and gap < rep["frame"]["target_bedtime_min_gap_minutes"]:
                j = str(d.get("transfer_justification", "")).lower()
                if d.get("inference_type") != "indirect" or not any(w in j for w in GAP_WORDS):
                    fail("R4", f"{fid} ({sid}, bedtime gap {gap} min) is used against bedtime; it must be declared "
                               f"indirect with a bridge that addresses the shorter gap")
        if fav == h1 and facts is not None:              # the same bridge duty for favourable trials (symmetry)
            mg = facts.get("morning_gap_minutes")
            if mg is not None and mg < rep["frame"]["target_morning_min_gap_minutes"]:
                j = str(d.get("transfer_justification", "")).lower()
                if d.get("inference_type") != "indirect" or not any(w in j for w in GAP_WORDS):
                    fail("R4", f"{fid} ({sid}, morning gap {mg} min) is used for bedtime; it must be declared indirect "
                               f"with a bridge that addresses the shorter morning comparator")
        if fav != h1 and facts is not None:
            if facts.get("pooled"):
                if "stratum" not in str(d.get("transfer_justification", "")).lower():
                    fail("R18", f"{fid}: a pooled trial average used against bedtime must say which exposure stratum it "
                                f"can bear on (unconditioned averages do not answer the interference stratum)")

    led = rep.get("exposure_ledger") or {}
    for side in ("morning", "bedtime"):
        rows = {r.get("factor"): r.get("status") for r in led.get(side, []) if isinstance(r, dict)}
        missing = [f for f in LEDGER_FACTORS if rows.get(f) not in LEDGER_STATUS]
        if missing:
            fail("R7", f"{side} ledger lacks a status for: {', '.join(missing)}")

    strata = rep.get("stratified_conclusions") or {}
    for s in STRATA:
        if not str((strata.get(s) or {}).get("conclusion", "")).strip():
            fail("R19", f"missing stratified conclusion for '{s}'")
    safety = rep.get("safety") or {}
    for s in SAFETY:
        if safety.get(s) in (None, "", False):
            fail("R20", f"safety block lacks '{s}'")
    if not str(rep.get("decision_to_offer", {}).get("conclusion", "")).strip():
        fail("R21", "the decision-to-offer conclusion must be stated separately from efficacy")
    return errors


CONTRACT = v1.CONTRACT.replace('"weighting_method": "holistic_study_and_comparison_assessment | count_frds"}}',
 '"weighting_method": "holistic_study_and_comparison_assessment | count_frds",\n'
 ' "stratified_conclusions": {"documented_removable_morning_interference": {"conclusion": ""},\n'
 '                            "persistent_non_timing_cause": {"conclusion": ""},\n'
 '                            "no_documented_interference": {"conclusion": ""}},\n'
 ' "safety": {"overreplacement_recheck_weeks": 6, "bedtime_interferents_checked": true, "sampling_time_standardised": true,\n'
 '            "no_dose_change_at_switch": true, "high_risk_groups_named": true},\n'
 ' "decision_to_offer": {"conclusion": ""}}}') + (
 "\nThe exposure_ledger must list every one of these factors on BOTH schedules, each with status measured | reported | "
 "inferred | unknown: " + ", ".join(LEDGER_FACTORS) + ". Every FRD listed as a driver in the allocation block must appear in "
 "gate_report.drivers with the same direction. Documents listed as synthesis sources can never be drivers.")
