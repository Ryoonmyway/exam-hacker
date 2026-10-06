# Shared Markdown learning record

Read this for course-state work. All six specialists use this one reference; find it through the installed `exam-hacker` skill or the sibling directory in the collection. Do not copy it into six slightly different contracts.

## Files and authority

```text
course-root/
  reference/                    original course materials
  progress/
    progress.md                 current decisions and resumption entry
    materials.md                source index and inspected coverage
    notes/<block-or-problem>.md  one authoritative explanation
    practice/<task-id>.md        question, attempts, feedback
```

Create only files needed now. Standalone notes or solutions may omit the progress entry. Never create JSON/JSONL learning files, hidden JSON blocks, or a second machine version. Platform skill configuration is not a learning record.

Use descriptive stable task/topic/source IDs and Markdown links. A progress row summarizes the current conclusion and links to its evidence; do not paste the entire attempt or lecture into it. Use the course language, including headings. The examples below are a small organizational convention, not a demand to fill an empty schema.

## Math formatting

In saved Markdown, put each display-math `$$` delimiter on its own unindented line, with the formula between the two lines and blank lines outside the block. Do not attach opening or closing delimiters to a formula line, especially for multiline derivations: some previews then consume subsequent prose as math. Keep headings and explanatory paragraphs outside math blocks. For chat replies, use paired `\(` / `\)` inline and `\[` / `\]` for displays, without mixing delimiter styles within a formula.

Before delivery, check delimiter pairing and block boundaries. When rendering tools are available, check the complete Markdown through a math-aware parser and KaTeX, not just isolated TeX expressions; verify that following headings and prose remain outside the formula. A successful learning-record check alone does not validate formula rendering.

## Progress entry

Use these sections (Chinese/English headings shown for the optional checker):

- `目标与约束 / Goal and constraints`: course, goal, absolute exam date and timezone when known, user-confirmed remaining time, source and uncertainty. Missing facts remain unknown. Record when capacity was confirmed; elapsed wall time is not observed study time.
- `掌握与优先级 / Mastery and priorities`: capability, observed/self-reported ability, confidence, evidence link, P0/P1/P2 with reason, repair action and pass condition. Exam importance is separate from ability.
- `当前任务 / Current task`: stable task ID and link, objective, stage, what is awaiting the learner, hint/answer exposure, and relevant note/source links. Explicitly say no pending task when none exists. Never infer “awaiting answer” merely because a planned Session exists.
- `下一步 / Next action`: one concrete next action; optional short pass/fail branches, not an exhaustive calendar.
- `最近更新 / Recent changes`: dated material changes, their evidence links, and pending/unresolved corrections.

Record `剩余分钟 / Remaining minutes` and `下一任务分钟 / Next task minutes` as plain numeric list fields when known. An estimate is not user-confirmed capacity. If the chosen task exceeds known capacity, shorten it or explain the unavoidable mismatch and ask for the decision.

## Sources

In `materials.md`, record source ID, real path/link or user statement, authority, inspected portion, method, usable anchors, and gaps. Cite exact pages/headings/questions. Generated exercises and notes are outputs, not independent evidence of exam scope or historical frequency.

For scanned/mixed PDFs, preserve the readability and rendered-page protocol in the triage references: actual 1-based pages inspected, targeted/full coverage, method, and OCR's navigation-only role. Record these as readable Markdown, not nested data objects. Never imply whole-document coverage after a partial inspection.

## Practice records and feedback

A task file contains:
- ID, topic, objective, origin (original/adapted/generated), source basis, verification status, estimated effort, and pass criteria;
- exact self-contained prompt and any figure or givens necessary to resume;
- actual answer exposure and hints, including when these changed;
- dated attempts with stable IDs (e.g. `### Attempt A01`), the user's work or its faithful reference, conditions, feedback, and grading basis;
- later corrections with their own IDs and an explicit link to the corrected observation.

Before the first attempt, save the question and verification receipt without solutions or answer-bearing hints in the learner-facing file. Verify generated answers privately before presentation; do not save an answer key next to an unanswered task or put it in a spoiler. This is an instructional boundary, not an access-control system.

Append observations; do not overwrite earlier mistakes or historical evidence. When the same submission is already recorded, reuse that attempt; a new hint or correction is a new event, not a duplicate score. Keep “task attempted/completed” separate from “criterion passed”.

Levels may summarize evidence:
- 0: cannot start or recognize the method;
- 1: proceeds with major hints/answer exposure;
- 2: independently completes a standard task;
- 3: completes an appropriate timed variant and explains conditions.
Unknown remains unknown. A single task supports only the tested capability and conditions. Self-report stays labeled; exposed-answer practice cannot establish independent mastery.
An important but untested capability is a provisional assessment need, not a confirmed P0 defect. P0 requires evidence of a blocker (or an essential missing input that really prevents the current task).

## Who updates what

The active operator saves information it just produced. Drill owns its observation/feedback; compress and solve own their notes; triage establishes course decisions; replan revises consequential course decisions. Any active operator may update the pending-task pointer and resumption fields it actually changed. Router orchestration is sequential; there is no multi-writer protocol to maintain.

On each actionable feedback message, record the observation before planning from it. Update immediate explanation/task support even if no global replan is needed. Invoke replan when evidence changes priorities, future task selection, capacity, abandonment, or completion. An unchanged self-report need not rewrite the whole plan.

Save the pending task before ending a turn that asks for an answer. On partial write failure, report what did/did not persist and repair from the existing record on resume. Do not claim a successful save from an intention or tool call alone.

Before editing, read the current file so user edits are respected. After saving, inspect the changed entries and links. Where useful run:
```text
python <exam-hacker>/scripts/check_learning_record.py <course-root>
```
This checks local links, duplicate attempt headings, and the explicitly recorded next-task capacity. It does not certify pedagogy, source truth, mathematical correctness, or mastery.

## Context and recovery

New chat: read progress, then the pending task and its latest relevant feedback; follow other links only as needed. On context pressure or a natural block boundary, save the same checkpoint and provide a pasteable resume sentence containing the actual course path. Do not invent context-token thresholds or open a new chat without request.

Keep the entry concise. Move older change history to a linked Markdown history file when it impedes reading. Do not read full historical logs by default. Actual question text, answer exposure, raw observations, and unresolved corrections must remain recoverable.
