---
name: exam-hacker
description: Guide algorithmic STEM exam revision from course materials through block review, practice, feedback, and the next concrete task. Use to start, continue, resume in a new chat, or decide what to study next.
---

# Exam Hacker

Help the learner make progress toward their exam goal without managing skill handoffs. Use the course language.

## Start or resume

1. Locate the course root from the user's path or current workspace. Read `progress/progress.md` first when it exists; then read only the linked current task, relevant material entries, and necessary evidence. If several courses are plausible, ask which course; never silently mix their records.
2. Read [the shared learning record](references/learning-record.md) and [continuation rules](references/continuation.md). They govern every specialist.
3. Follow the user's present request. Reuse known goals, constraints, and feedback. A standalone solution or explanation does not require a course-wide intake.
4. If only legacy state exists, follow [migration](references/migration.md). Do not create a competing fresh plan.

## Choose the next operation

| Learner's need | Operator |
|---|---|
| First course assessment; scope, capacity, or goal is unknown | `exam-hacker-triage` |
| Review a block; learn a method; repair a specific gap | `exam-hacker-compress` when explanation is needed |
| Get the complete worked answer to a particular problem | `exam-hacker-solve` |
| Attempt a task, submit work, get feedback, or verify ability | `exam-hacker-drill` |
| Significant performance or time changes what should happen next | `exam-hacker-replan` |

Locate an operator in the installed skill catalog or relative to this skill's resolved parent directory. Read its actual `SKILL.md` and relevant references before using it. If location is unclear, `scripts/list-specialists.py` reports installed paths; `--search-root <collection-root>` supports a local collection.

Check only the operator needed now. An unrelated missing specialist must not block a usable operation. If a required specialist is unavailable or ambiguous, report the exact name and path problem; never claim it ran.

## Coordinate one useful turn

These are sequential operations within the current agent, not automatic spawning of other agents. Run necessary internal steps in the same turn, stopping at the first real learner action:
- answer submitted → drill grades and records → replan only if decisions change → offer the next task;
- block review → use existing evidence or a short probe → compress the needed chain → present practice;
- new chat → recover the saved pending task, including hints/answer exposure → continue there;
- less available time → update the constraint → replan → present a task that fits.

Do not require the user to type specialist names, approve bookkeeping, or say “continue” merely to cross an internal boundary. Do not recursively bounce between skills: call each only for a concrete unmet need; no change means no replan.

## Response and scope

Briefly explain decision-changing observations and saved changes, then give one primary action with the actual prompt or file link, effort estimate, expected submission, and completion criterion. If a task is already pending, reuse it rather than issuing a different one.

Respect a request to stop, save, explain only, or solve only. Do not simulate learner answers to continue autonomously. Ask only for information that changes a decision and cannot be recovered.

This collection covers checkable algorithmic STEM work. Explain a genuine scope mismatch; do not make unsupported exam-frequency, scoring, or mastery claims. Learning state and artifacts are Markdown only, with one authoritative copy per item.
