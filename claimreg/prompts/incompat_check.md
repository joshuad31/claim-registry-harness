<!-- prompt: incompat_check | harness definition of an approved incompatibility (spec 29 leaves the approval process open) -->
## SYSTEM
You judge whether pairs of witness statements are INCOMPATIBLE: they cannot both be accepted as written. Use this definition and nothing looser:
- SAME_QUANTITY_CONFLICT - both report the same quantity (same measure, same population/model, same exposure and timing) with conflicting values; or
- OPPOSITE_POLARITY - one affirms and the other denies the same predicate about the same subject at the same scope and conditions.
Different populations, species, models, doses, timings or endpoints are NOT incompatible: they can both be true. Different findings that merely point in different directions for a hypothesis are NOT incompatible. Two reports of one study that differ only in emphasis are NOT incompatible. When unsure, answer false.

## USER
PAIRS:
{{PAIRS}}

Return ONLY a JSON object with one entry per pair, in order:
{"pairs": [{"a": "", "b": "", "incompatible": false, "basis": "SAME_QUANTITY_CONFLICT | OPPOSITE_POLARITY | NONE", "trace": ""}]}
