<!-- prompt: match_adjudicate | v2: chooses between the two passes or abstains | resolves pass A/B disagreements for one unit; recorded as MODEL_ADJUDICATED, never as agreement -->
## SYSTEM
Two independent reviewers assigned different relations to the witness-unit pairs listed below. For each pair, decide which of the two reviewers' relations the texts actually support, or ABSTAIN. You choose between pass A's answer and pass B's answer; a third relation that neither reviewer gave is not accepted and the pair is then left undecided. Do not average or split the difference. When the stronger relation depends on an assumption the witness does not state, choose the weaker relation.

{{> match_relations.md}}

## USER
COVERAGE UNIT {{UNIT_ID}} ({{UNIT_TYPE}}) of hypothesis {{HID}}:
"{{UNIT_TEXT}}"

DISPUTED PAIRS:
{{DISPUTES}}

Return ONLY a JSON object with one decision per disputed pair:
{"unit_id": "{{UNIT_ID}}", "decisions": [{"witness_id": "", "relation": "", "trace": "", "gap_type": "", "gap": "", "agrees_with": "A | B | neither"}]}
