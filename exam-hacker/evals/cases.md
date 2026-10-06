# Behavioral evaluation

Use isolated disposable courses and real skill instructions. Give evaluators only the user request and raw inputs; do not preload expected answers. Do not simulate learner responses. Follow up with the explicitly supplied test response.

## Scenarios

| ID | User situation | Observable acceptance |
|---|---|---|
| start-no-bank | Known topic, short capacity, only verified theory | Suitable verified generated task; no forced question upload; actual prompt and saved pending state |
| feedback-repair | Wrong lever arms with explicit confusion | Grade against source logic; save actual work; explain the localized gap; present a new task |
| shortened-time | Same feedback says only six minutes remain | Use the new capacity; fit the next task; preserve earlier evidence |
| resume-exposed | New chat; learner says a visible answer was understood | Recover exact exposure; keep self-report distinct; present a fresh verification task |
| solution-only | Learner explicitly requests full answer and no next exercise | Full checked answer; save exposure; no mastery upgrade or forced task |
| source-gap | Neither topic boundary nor course evidence is available | Ask only the decision-bearing minimum; label general practice if chosen |
| scanned-source | Image-only formula/problem/rubric | Render and inspect exact pages; anchor claims to viewed pages, not OCR |
| migration | Old state, logs, artifacts and unfamiliar metadata | Preview is read-only; preserve fields/bytes; no invented pending attempt; only MD active |
| interrupted-write | Archive/removal failure | Restore byte-identical inputs, remove only new outputs, report failure |
| scope-correction | New source changes scope on an existing course | Audit source; update affected decisions without resetting history |

The file-operation cases run with `python exam-hacker/evals/test_learning_records.py`. Forward traces and limitations are recorded in [the latest evaluation](results/2026-09-30-refactor.md).

A metadata pass or green file checker does not establish mathematical or teaching quality. Inspect the actual question, response, and saved state. Acceptance of the refactor requires all seven implementation areas plus evidence for the representative behaviors above, not matching fixed response wording.
