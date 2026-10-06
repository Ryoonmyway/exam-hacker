---
name: exam-hacker-drill
description: Select or generate a suitable STEM exercise, present it without answers, grade the learner's work, update Markdown progress, and provide the next task. Use to practice, test understanding, or submit answers.
---

# Exam Hacker Drill

Turn the current objective into observable learning and an actionable next step.

Read the shared `exam-hacker/references/learning-record.md` and `continuation.md`. Read [question design](references/question-design.md) when selecting/generating tasks and [feedback](references/loop-state-contract.md) when responding to work.

## Recover or start

Read `progress/progress.md` and its pending practice file. Recover exact givens, hints/answer exposure, attempts, objective and remaining time. If an unanswered task exists, resume it unless the user changes the request.

A standalone request to practice a named topic can use a minimal practice record without a full strategy. If scope is too vague to select valid content, ask the smallest necessary question. For a new exam-wide plan use triage.

Choose a task that can teach or discriminate the relevant capability. Use existing course problems, adapted problems, or verified generated problems according to the question reference. A missing question bank is not a stopping condition.

## Present and persist

Verify the problem before presenting it. Save the exact prompt, origin, source basis, pass condition, estimate, and exposure state in `progress/practice/<task-id>.md`. Update the progress pointer when a course entry exists.

Present the actual task, expected submission, effort estimate and pass criterion. Do not reveal answers, worked steps, or answer-bearing hints before an attempt unless requested. If hints are requested, give useful graduated help and record it; do not pretend later assisted work was independent.

Stop at the learner's answer. Never generate an imaginary attempt to complete the loop.

## Grade and respond

Match work to the pending task. If the mapping is genuinely ambiguous, ask which task; do not guess and mutate another record.

Compare with verified source answers or independently checked reasoning. Distinguish official grading from agent-derived correctness judgments. Cite the basis. Do not invent process marks. Separate conceptual/method errors, arithmetic, notation, and ambiguous work.

Save the actual observation and feedback immediately. Preserve self-report, assisted practice, independent performance, and time conditions distinctly. Repeated submission of the same recorded work does not create another mastery event. Corrections append a new dated entry referring to the prior one.

Update the tested capability, uncertainty, current task state and next pointer in Markdown. Replan only if the result changes course decisions. A failure to meet criteria does not become a pass just because the task ended.

## Next action in the same turn

- Specific method gap → compress the necessary repair, then give a new small task.
- Sufficient standard performance → give an appropriate variant or timed check if useful.
- Goal/criterion achieved → close the block or move to the next planned one.
- Time/priority changed → replan, then present the selected task.
- “I understand” without work → record self-report and give a short verification when it matters.

Honor a request to grade only or stop. Otherwise do the next operation and present its actual task; do not end by telling the user to call another skill.
