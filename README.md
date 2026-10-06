# Exam Hacker

English | [简体中文](README.zh-CN.md)

Repository: [Ryoonmyway/exam-hacker](https://github.com/Ryoonmyway/exam-hacker)

An exam-review skill collection for checkable STEM calculations, derivations, and proofs. State your goal, submit work, or say “continue”; the agent recovers progress and proceeds to the next concrete learner action.

## Choose by need

| What you need | Direct entry |
|---|---|
| Start, decide where to begin, or resume a new chat | `$exam-hacker` |
| Diagnose priorities and realistic capacity | `$exam-hacker-triage` |
| Review a block's method or repair a specific gap | `$exam-hacker-compress` |
| Read a complete checked worked solution | `$exam-hacker-solve` |
| Get exercises, submit answers, or verify understanding | `$exam-hacker-drill` |
| Adjust future work after evidence/time changes | `$exam-hacker-replan` |

You do not need to manage specialist handoffs. Each turn ends at a real task with an effort estimate, expected submission, and pass condition. Explicit requests to explain only, solve only, or stop are respected.

## Learning flow

Initial assessment → current block → explanation where needed → practice → record feedback → adjust where needed → next task.

Use existing performance instead of forcing a diagnostic before every block. P0 blocks the current goal; P1 is a consequential present loss; P2 can wait. Priority depends on goal relevance, evidence, prerequisites, and time, not simply an ability score.

“I understand” is saved as self-report, not verified mastery. Suitable original, adapted, and checked generated exercises are supported; no supplied question bank is required. A visible worked example requires a fresh task for later independent verification.

## Markdown is the learning record

```text
course-root/
  reference/
  progress/
    progress.md
    materials.md
    notes/<block-or-problem>.md
    practice/<task-id>.md
```

Create only needed files. Maintain one authoritative copy per item and link to it. No learning JSON/JSONL, hidden JSON blocks, or synchronized machine/display copies. Platform YAML configuration is separate.

Save the exact pending question and exposure conditions before waiting. Record feedback as it arrives, preserve attempts, and append corrections. Keep the progress entry concise and read linked history only when needed.

In a new chat in the same course folder:
```text
Use $exam-hacker to continue this course. Read progress/progress.md and resume the pending task.
```
Include the absolute course path if the new chat is elsewhere. Recovery requires access to those files; the skill does not automatically open chats.

## Examples

```text
Use $exam-hacker to start structural mechanics review. My exam date is ...,
target is ..., and I can actually spend ... minutes. Materials are in reference/.
Start the first useful learning task.
```

```text
Use $exam-hacker-compress to review the force-method block.
Use my existing work to focus the explanation, then let me practice.
```

```text
Use $exam-hacker-drill to test compatibility conditions.
I have course notes in reference/ but no question bank.
```

```text
Use $exam-hacker-solve to give the complete answer to this problem. Explanation only this time.
```

## Install from a local checkout

Get the code from the repository above, then run this from its local root directory (requires Node.js and npx):
```bash
npx -y skills add . -g --all
```

Start a new chat after installation. Install all six skills for the full workflow; specialists share record and continuation guidance in the entry skill. Only the currently needed capability is checked, so unrelated missing specialists do not block useful work.

## Legacy import

Follow [the migration reference](exam-hacker/references/migration.md) for legacy strategy.json and mastery-evidence.jsonl. Preview, then apply once. The helper verifies a recovery ZIP before removing the exact legacy input files; only Markdown is maintained afterward. Conflicting current/legacy records are reconciled, not overwritten.

```text
python <exam-hacker>/scripts/migrate_legacy.py <course-root>
python <exam-hacker>/scripts/migrate_legacy.py <course-root> --apply
```

## Evidence boundaries

Exam scope, weights, and instructor emphasis need sources. Self-reported ability is not exam-value evidence. Strategic abandonment needs evidence, capacity tradeoffs, downside, and a reversal condition.

Inspect rendered scanned pages; OCR only locates. Partial inspection cannot establish whole-document claims. Label generated exercises and agent-derived answers honestly; never fabricate official rubrics or process marks.

The collection targets checkable algorithmic STEM work, not unconstrained essays.

## Validation

```text
python exam-hacker/evals/test_learning_records.py
python exam-hacker/scripts/check_learning_record.py <course-root>
```

These check import/rollback and concrete record invariants, not pedagogy or mathematical truth. See [behavior scenarios](exam-hacker/evals/cases.md) for behavioral evaluation and actual results.
