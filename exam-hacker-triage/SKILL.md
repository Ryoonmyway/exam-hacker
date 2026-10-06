---
name: exam-hacker-triage
description: Quickly decide what to study first for an algorithmic STEM exam using course evidence, current ability, and remaining time, with explicit confidence. Use for a new course, missing exam context, or a source audit; no full-course ability test by default.
---

# Exam Hacker Triage

Establish a useful first decision and assess confidence in it. A request for a complete diagnosis broadens the review coverage; it does not by itself request a full-course ability test.

Read the sibling/installed `exam-hacker/references/learning-record.md` and `continuation.md`. Existing Markdown state comes first; if only old state exists, use the shared migration reference.

## Intake and sources

Recover course, target, exam date/timezone, realistic remaining study time, materials, and known performance. Ask only for missing facts that change the choice. If the user wants a standalone explanation or problem solution, send that request directly to compress or solve without course-wide intake.

Read [evidence rules](references/evidence-contract.md). Inspect actual material, recording sources and gaps in `progress/materials.md`. Scope, score weights, and teacher emphasis need verified sources or explicitly labeled user statements.

For PDFs run `scripts/inspect_pdf_readability.py`. If visual follow-up is required, read [the scanned-PDF protocol](references/scanned-pdf-protocol.md), render decision-relevant pages, and inspect them visually. OCR only locates. A targeted inspection supports only those pages.

Read [confidence intake](references/mastery-snapshot.md). Reuse recent work and feedback; use a roughly one-minute self-report when needed, without requiring exercises first. Missing ability evidence is unknown, not zero. Low confidence alone does not trigger testing; normally calibrate through subsequent learning.

## Diagnose and choose

Keep exam relevance, mastery gap, learnability, and time cost separate. Rank concrete problems by the current goal:
- P0: blocks the chosen goal/task, including a critical prerequisite;
- P1: a consequential and currently worthwhile loss of marks or transfer;
- P2: local accuracy/speed/polish that can wait.

Do not map ability levels directly to priorities. A difficult out-of-scope topic is not P0. Importance or untested ability alone does not prove a P0 blocker: record the uncertainty, not a confirmed learning defect or an automatic testing task. Label uncertain rankings provisional. Each finding needs evidence, qualitative confidence with its reason, impact, next repair, and a pass condition. Do not fabricate precise expected-score gains.

Apply the abandonment gate in the evidence reference. Without its conditions, defer provisionally and state the risk; do not claim that absence from a small sample means low frequency.

## Save and launch

Use [the planning reference](references/strategy-contract.md) to write `progress/progress.md`. Name the current block, first objective, capacity, evidence, and next action. Retain only a small useful look-ahead.

Give the provisional diagnosis before launching learning; do not withhold useful priorities until every capability is verified. If the user requested diagnosis only, return the findings and a concrete recommended next action. Otherwise, in the same turn invoke compress if the first learning task needs a method scaffold, or drill for practice. A diagnostic probe must pass the confidence reference's gate. A source-backed generated exercise is valid when there are no original questions. If both scope and theory are unknown, obtain the minimum topic boundary or label agreed general practice honestly.

For an existing course, add newly audited sources and update factual corrections in place with a dated receipt; use replan for resulting changes in priorities. Never reset completed work just because new material arrived.

For learning requests, end at the first learner action, following the shared continuation rules. For diagnosis-only requests, stop after the findings and recommended next action. Do not stop at “plan saved, now call drill.”
