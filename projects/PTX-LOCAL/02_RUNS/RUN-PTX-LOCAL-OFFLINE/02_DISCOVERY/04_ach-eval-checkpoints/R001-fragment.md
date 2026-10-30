---
artifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT
revision: 1
---

Local-engine checkpoint for round 1. The allocations below are a bookkeeping split of the gauge over the frozen hypotheses, computed from the cumulative count of answer blocks that share terminology with each hypothesis. They are not an ACH_Eval judgment. Substantive conditions: local engine: 7/11 decisive tests, 2/6 hypotheses adversely tested, 4/6 assumptions touched, 0/6 corroboration contexts touched.

```json
{
 "allocations": {
  "A1": {
   "A1-H1": 20,
   "A1-H2": 30,
   "A1-H3": 14
  },
  "A2": {
   "A2-H1": 27,
   "A2-H2": 21,
   "A2-H3": 16
  }
 },
 "evidence_counts": {
  "A1-H1": 1,
  "A1-H2": 3,
  "A1-H3": 0,
  "A2-H1": 2,
  "A2-H2": 1,
  "A2-H3": 0
 },
 "basis_confidence": {
  "A1": "local bookkeeping",
  "A2": "local bookkeeping"
 },
 "substantive_conditions": {
  "decisive_tests_oriented": true,
  "every_live_hypothesis_adversely_tested": false,
  "weakest_and_shared_links_tested": true,
  "project_success_conditions_addressed": false,
  "notes": "local engine: 7/11 decisive tests, 2/6 hypotheses adversely tested, 4/6 assumptions touched, 0/6 corroboration contexts touched"
 },
 "direction": "CONTINUE",
 "feedback_packet": {
  "expected_return": "rising",
  "posture": "query sources that have not yet been named; test the weakest required part",
  "priorities": [
   {
    "id": "P-1",
    "finding_or_gap": "sources named once and never cited",
    "missing_material": "a source-attributed finding for an unqueried named source",
    "question": "What does the source report about the required part it was named for?",
    "sources": [],
    "success_criterion": "a usable, cited answer",
    "affects": "coverage of the named hypothesis parts"
   }
  ],
  "substantial_novelty": "new source-attributed findings from newly named sources",
  "trivial_novelty": "restatements of findings already recorded",
  "open_gaps_and_corrections": [
   "local engine: 7/11 decisive tests, 2/6 hypotheses adversely tested, 4/6 assumptions touched, 0/6 corroboration contexts touched"
  ],
  "answers_needing_repair": [],
  "holds": "none"
 }
}
```
