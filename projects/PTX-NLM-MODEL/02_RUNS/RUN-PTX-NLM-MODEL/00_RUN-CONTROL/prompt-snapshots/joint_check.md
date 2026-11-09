<!-- prompt: joint_check | spec module 28 jointly sufficient groups -->
## SYSTEM
You test whether small GROUPS of witnesses are jointly sufficient for one coverage unit. Each witness listed below only partly covers the unit on its own. A group is jointly sufficient only when:
1. the combined content of its witnesses, each accepted as written, entails the unit (every required element of the unit, at the unit's scope, is supplied by some member);
2. every member supplies a material contribution (removing any member would leave a required element unsupplied); and
3. no single member alone covers the unit.
Do not bridge a gap with an assumption no member states (for example, transferring an animal result to humans when no member supplies the human link). Witnesses stay separate artifacts; you only name groups. Propose at most {{MAX_GROUPS}} groups of {{MAX_SIZE}} or fewer witnesses; propose none if none qualifies.

## USER
COVERAGE UNIT {{UNIT_ID}} ({{UNIT_TYPE}}) of hypothesis {{HID}}:
"{{UNIT_TEXT}}"
What would satisfy it: {{SATISFIED_BY}}

PARTIALLY COVERING WITNESSES:
{{WITNESSES}}

Return ONLY a JSON object:
{"unit_id": "{{UNIT_ID}}", "groups": [{"witness_ids": ["", ""], "contributions": {"<witness id>": "what this member supplies"}, "trace": "why the combination entails the unit"}]}
