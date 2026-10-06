---
name: exam-hacker-solve
description: Give a complete checked solution to one algorithmic STEM problem, explaining the method and its limits. Use when the learner requests the answer or a worked example; visible solutions are practice, not proof of mastery.
---

# Exam Hacker Solve

Provide the full requested solution without a compulsory attempt.

Read the shared `exam-hacker/references/learning-record.md` and `continuation.md`, plus [solution guidance](references/artifact-contract.md).

Recover the exact statement, givens, diagram, sources and requested endpoint. A standalone problem needs no strategy or course intake. If an essential given is missing, identify it; use assumptions only when authorized and label their consequences.

For sparse/scanned sources, render and inspect the relevant pages, including diagrams and answer annotations. OCR alone cannot verify them.

## Solve and check

Translate the problem into a reproducible sequence with conditions, sign conventions, intermediate results and meaningful checks. Give the full answer directly.

Classify the result:
- reference verified: checked against a verified answer source;
- agent derived: no verified answer; checked by meaningful independent methods;
- partially verified: only limited checking possible, with the remaining uncertainty explicit.

Never label a failed endpoint as a completed valid solution or invent official process marks.

Save one Markdown solution at `progress/notes/<problem-id>-solution.md` when persisting work. Do not produce a JSON counterpart. Link to exact sources and state applicability/failure boundaries.

## Exposure and continuation

If this was a pending unanswered task, record that the answer was revealed and link the solution from its practice record. Preserve earlier independent attempts; work after exposure is assisted practice.

Generating or reading a solution does not upgrade mastery. For an ongoing review session, drill may now present a fresh verified transfer task in the same turn. For an explicit solution-only request, finish the solution and stop; do not force further study.

If the user asks only about one step, compress may provide the local repair rather than reproduce the entire answer. Keep the user-facing next action concrete whenever continuation is appropriate.
