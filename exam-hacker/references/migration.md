# One-time legacy import

Use only when old Exam Hacker JSON/JSONL learning files exist and the Markdown progress entry does not. Do not restart a course or maintain two active formats.

The helper accepts the supported legacy strategy shape (course, planning context, materials, mastery, actions, loop state), event logs, and compress/solve artifacts:

```text
python <exam-hacker>/scripts/migrate_legacy.py <course-root>
python <exam-hacker>/scripts/migrate_legacy.py <course-root> --apply
```

The first command previews files and warnings without writing. Inspect that output and source identity. Use `--strategy <relative-path>` only to choose a known historical snapshot when there is no canonical `progress/strategy.json`; never guess between revisions.

On apply the helper:
- checks input readability and refuses to overwrite an existing Markdown entry;
- renders current progress, materials, imported observations and complete historical field values to Markdown;
- imports artifact information without keeping a JSON mirror;
- validates the proposed Markdown links and explicit capacity fields;
- makes a ZIP recovery backup and verifies every archived input byte;
- removes only the exact backed-up legacy learning files under this course root.

The ZIP is an inactive recovery backup, not a second maintained version. No normal skill reads it. Existing non-JSON course materials and notes are preserved. The helper never scans other course directories.

## Review before continuing

Read the import summary and warnings. A legacy plan may identify a Session without saving its question text, hint state, or pending answer; mark that resume gap rather than inventing an active attempt. Ask only for the missing information necessary to continue, or start a new suitable task with the user's request.

Imported sources retain legacy verification labels, but this import does not re-read or reconfirm source truth. Missing paths become explicit gaps. A dated plan may be stale: confirm goal/capacity only when its age or contradictions change the next decision.

The historical Markdown export preserves every legacy scalar field, including unfamiliar ones, for review; it is not a schema the learner must maintain. Current decisions are edited only in progress.md. Do not use old numeric priority labels as automatic new P0/P1/P2 assignments.
Legacy display notes may omit conditions or checks that existed only in their former structured artifact. Before teaching from such a note, read that artifact's section in the imported history and consolidate the necessary explanation into the same note; do not assume the old display was complete or create a second maintained copy.

If existing Markdown and legacy state disagree, stop automatic migration and reconcile the concrete conflicting records. Do not silently overwrite either.

If import fails, report the exact phase and preserve the original data. A helper failure never authorizes deleting a source file or fabricating a successful continuation.
