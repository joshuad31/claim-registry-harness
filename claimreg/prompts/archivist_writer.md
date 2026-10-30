<!-- prompt: archivist_writer | Archivist custom prompt generator v4 (verbatim, spec 04) -->
## SYSTEM
{{> spec/Archivist_Prompt_Generator_v4.md}}

## USER
SUPPLIED HEADER OR TOPIC DESCRIPTION (hypotheses, ranks and decisive tests must NOT appear in your output):
<<<HEADER
{{HEADER}}
HEADER>>>

SOURCE LIST / INDEX (for corpus-specific guardrails):
<<<INDEX
{{INDEX}}
INDEX>>>

Return only the finished custom prompt, from "You are" through its last OUTPUT bullet.
