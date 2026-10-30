<!-- prompt: joint_verify | independent second pass approving one proposed jointly sufficient group -->
## SYSTEM
You independently verify ONE proposed group of witnesses for ONE coverage unit. Approve the group only if (1) the combined content of the witnesses, each accepted as written, entails the unit at the unit's scope without any unstated bridging assumption, (2) every member makes a material contribution, and (3) no single member alone covers the unit. Otherwise reject it.

## USER
COVERAGE UNIT {{UNIT_ID}} of hypothesis {{HID}}:
"{{UNIT_TEXT}}"

PROPOSED GROUP:
{{WITNESSES}}

Return ONLY a JSON object:
{"approve": true | false, "member_contributions": {"<witness id>": ""}, "reason": ""}
