---
artifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT
revision: 4
---

Local-engine checkpoint for round 4. The allocations below are a bookkeeping split of the gauge over the frozen hypotheses, computed from the cumulative count of answer blocks that share terminology with each hypothesis. They are not an ACH_Eval judgment. Substantive conditions: local engine: 7/11 decisive tests, 3/6 hypotheses adversely tested, 2/6 assumptions touched, 2/6 corroboration contexts touched.

```json
{
 "allocations": {
  "A1": {
   "A1-H1": 24,
   "A1-H2": 29,
   "A1-H3": 11
  },
  "A2": {
   "A2-H1": 38,
   "A2-H2": 19,
   "A2-H3": 7
  }
 },
 "evidence_counts": {
  "A1-H1": 3,
  "A1-H2": 4,
  "A1-H3": 0,
  "A2-H1": 13,
  "A2-H2": 5,
  "A2-H3": 0
 },
 "basis_confidence": {
  "A1": "local bookkeeping",
  "A2": "local bookkeeping"
 },
 "substantive_conditions": {
  "decisive_tests_oriented": true,
  "every_live_hypothesis_adversely_tested": false,
  "weakest_and_shared_links_tested": false,
  "project_success_conditions_addressed": false,
  "notes": "local engine: 7/11 decisive tests, 3/6 hypotheses adversely tested, 2/6 assumptions touched, 2/6 corroboration contexts touched"
 },
 "direction": "CONTINUE",
 "feedback_packet": {
  "expected_return": "stable",
  "posture": "query sources that have not yet been named; test the weakest required part",
  "priorities": [
   {
    "id": "P-4",
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
   "local engine: 7/11 decisive tests, 3/6 hypotheses adversely tested, 2/6 assumptions touched, 2/6 corroboration contexts touched"
  ],
  "answers_needing_repair": [],
  "holds": "none"
 }
}
```
