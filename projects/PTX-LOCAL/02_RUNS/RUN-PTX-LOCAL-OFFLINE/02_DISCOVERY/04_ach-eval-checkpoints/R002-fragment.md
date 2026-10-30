---
artifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT
revision: 2
---

Local-engine checkpoint for round 2. The allocations below are a bookkeeping split of the gauge over the frozen hypotheses, computed from the cumulative count of answer blocks that share terminology with each hypothesis. They are not an ACH_Eval judgment. Substantive conditions: local engine: 5/11 decisive tests, 2/6 hypotheses adversely tested, 3/6 assumptions touched, 3/6 corroboration contexts touched.

```json
{
 "allocations": {
  "A1": {
   "A1-H1": 20,
   "A1-H2": 30,
   "A1-H3": 14
  },
  "A2": {
   "A2-H1": 29,
   "A2-H2": 26,
   "A2-H3": 9
  }
 },
 "evidence_counts": {
  "A1-H1": 1,
  "A1-H2": 3,
  "A1-H3": 0,
  "A2-H1": 6,
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
  "project_success_conditions_addressed": true,
  "notes": "local engine: 5/11 decisive tests, 2/6 hypotheses adversely tested, 3/6 assumptions touched, 3/6 corroboration contexts touched"
 },
 "direction": "CONTINUE",
 "feedback_packet": {
  "expected_return": "rising",
  "posture": "query sources that have not yet been named; test the weakest required part",
  "priorities": [
   {
    "id": "P-2",
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
   "local engine: 5/11 decisive tests, 2/6 hypotheses adversely tested, 3/6 assumptions touched, 3/6 corroboration contexts touched"
  ],
  "answers_needing_repair": [],
  "holds": "none"
 }
}
```
