#!/usr/bin/env python3
"""Behavioral file-operation tests, using disposable courses only."""
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_learning_record import check
from migrate_legacy import migrate
import migrate_legacy

ENTRY = """# Review
## Goal and constraints
- Remaining minutes: 20
- Next task minutes: 5
## Mastery and priorities
Independent performance unknown.
## Current task
[Question](practice/Q01.md); awaiting answer; no hints or answers shown.
## Next action
Submit the equilibrium equations.
## Recent changes
Question presented; no attempt recorded.
"""
LEGACY = {
    "schema_version": 2,
    "course": {"id": "beam-course", "name": "梁", "target_score": 75},
    "planning_context": {"exam_date": "2026-10-02", "timezone": "Asia/Shanghai",
                         "availability": {"total_minutes": 60, "source": "user_confirmed"}},
    "source_materials": [{"id": "theory", "label": "Theory",
                         "path": "reference/theory.md", "inspection": {"pages_inspected": [2, 7]}}],
    "mastery_snapshot": [{"topic_id": "beam", "level": 1, "evidence_type": "self_report",
                          "notes": "看懂答案，并未独立作答"}],
    "priorities": [{"title": "梁", "level": "must_win", "reason": "Core prerequisite"}],
    "action_list": [{"id": "session-beam", "state": "active", "duration_minutes": 15,
                     "objective": "Find support reactions", "success_criteria": "Both equilibria"}],
    "loop_state": {"next_session_ids": ["session-beam"], "strategy_revision": 1},
    "custom_field": {"preserve_me": "独有标记-xyz", "empty": [], "nothing": None},
}
EVENT = {"event_id": "event-beam-001", "course_id": "beam-course", "evidence_type": "user_report",
         "result": {"level_observed": 1, "notes": "Needed hint; not independent"}}


class Records(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="exam-hacker-test-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def current(self):
        self.write("progress/progress.md", ENTRY)
        self.write("progress/practice/Q01.md", "# Q01\nA complete answer-hidden prompt.\n")

    def legacy(self):
        self.write("progress/strategy.json", json.dumps(LEGACY, ensure_ascii=False))
        self.write("reference/theory.md", "# Equilibrium\nSum forces and moments.")
        self.write("progress/mastery-evidence.jsonl", json.dumps(EVENT) + "\n")
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_valid_answer_hidden_record(self):
        self.current()
        self.assertEqual(check(self.root), [])

    def test_code_examples_do_not_create_links_or_attempts(self):
        self.current()
        example = "[example](missing.md)\n[ref][missing]\n### Attempt A01\n### Attempt A01\n"
        for start, end in [("```md", "```"), ("~~~md", "~~~"),
                           ("  ```md", "  ```"), ("````md", "````"),
                           ("~~~md", ""), ("```md", "")]:
            with self.subTest(fence=start, closing=end):
                self.write("progress/practice/Q01.md", f"{start}\n{example}{end}\n")
                self.assertEqual(check(self.root), [])
        for content in ["`[example](missing.md)`", "`` `[example](missing.md)` ``",
                        "`[example]\n(missing.md)`", "\n    " + example.replace("\n", "\n    "),
                        "\n\t[example](missing.md)\n"]:
            with self.subTest(content=content):
                self.write("progress/practice/Q01.md", content)
                self.assertEqual(check(self.root), [])

    def test_shorter_fence_does_not_end_example(self):
        self.current()
        self.write("progress/practice/Q01.md", "````md\n```\n[example](missing.md)\n````\n")
        self.assertEqual(check(self.root), [])

    def test_example_headings_do_not_satisfy_required_sections(self):
        self.current()
        for example in [f"```md\n{ENTRY}```\n", f"~~~md\n{ENTRY}~~~\n"]:
            with self.subTest(example=example):
                self.write("progress/progress.md", example)
                errors = check(self.root)
                self.assertEqual(sum("Missing progress section" in e for e in errors), 5)

    def test_example_capacity_does_not_override_real_capacity(self):
        self.current()
        self.write("progress/progress.md", "~~~md\n- Remaining minutes: -1\n~~~\n" + ENTRY)
        self.assertEqual(check(self.root), [])

    def test_real_links_after_code_are_still_checked(self):
        self.current()
        for code in ["~~~\n[example](fake.md)\n~~~", "`[example](fake.md)`",
                     "    [example](fake.md)\n"]:
            with self.subTest(code=code):
                self.write("progress/practice/Q01.md", code + "\n\n[real](absent.md)\n")
                errors = check(self.root)
                self.assertEqual(len(errors), 1)
                self.assertIn("missing linked path absent.md", errors[0])

    def test_unmatched_ticks_do_not_hide_other_blocks(self):
        self.current()
        self.write("progress/progress.md", "Unmatched `\n\n" + ENTRY + "\nAnother `\n")
        self.write("progress/practice/Q01.md", "Start `\n\n[real](absent.md)\n\nEnd `")
        errors = check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("missing linked path absent.md", errors[0])

    def test_code_label_and_indented_prose_keep_real_links(self):
        self.current()
        for text in ["[`question`](absent.md)", "A paragraph\n    [question](absent.md)",
                     "- A list item\n\n    [question](absent.md)"]:
            with self.subTest(text=text):
                self.write("progress/practice/Q01.md", text)
                errors = check(self.root)
                self.assertEqual(len(errors), 1)
                self.assertIn("missing linked path absent.md", errors[0])

    def test_parentheses_in_link_destinations(self):
        self.current()
        self.write("progress/practice/题目(修订(2)).md", "# Question")
        destinations = ["practice/题目(修订(2)).md", r"practice/题目\(修订\(2\)\).md",
                        "<practice/题目(修订(2)).md>",
                        'practice/题目(修订(2)).md "Title (revision)"',
                        "practice/题目(修订(2)).md (Title)",
                        "practice/题目%28修订%282%29%29.md"]
        for target in destinations:
            for link in [f"[question]({target})", f"[question][q]\n\n[q]: {target}"]:
                with self.subTest(link=link):
                    self.write("progress/progress.md", ENTRY + "\n" + link)
                    self.assertEqual(check(self.root), [])

    def test_missing_parenthesized_path_is_reported_in_full(self):
        self.current()
        self.write("progress/practice/Q01.md", "[missing](absent(rev(2)).md)")
        self.assertTrue(any("missing linked path absent(rev(2)).md" in e for e in check(self.root)))

    def test_invalid_utf8_specialist_is_reported_without_aborting_discovery(self):
        for name in ("triage", "compress", "solve", "drill", "replan"):
            self.write(f"exam-hacker-{name}/SKILL.md", f"---\nname: exam-hacker-{name}\n---\n")
        (self.root / "exam-hacker-triage/SKILL.md").write_bytes(b"---\nname: \xff\n---\n")
        script = Path(__file__).resolve().parents[1] / "scripts/list-specialists.py"
        for strict in (False, True):
            with self.subTest(strict=strict):
                result = subprocess.run([sys.executable, "-X", "utf8", str(script), "--search-root",
                                         str(self.root)] + (["--strict"] if strict else []),
                                        capture_output=True, encoding="utf-8")
                self.assertEqual(result.returncode, int(strict))
                self.assertIn("MALFORMED: exam-hacker-triage", result.stdout)
                self.assertIn("UTF-8", result.stdout)
                self.assertIn("AVAILABLE: exam-hacker-replan", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_unicode_headings_and_space_links(self):
        self.current()
        text = ENTRY
        for en, zh in [("Goal and constraints", "目标与约束"), ("Mastery and priorities", "掌握与优先级"),
                       ("Current task", "当前任务"), ("Next action", "下一步"), ("Recent changes", "最近更新")]:
            text = text.replace(en, zh)
        text = text.replace("practice/Q01.md", "<practice/题目 01.md>")
        self.write("progress/progress.md", text)
        self.write("progress/practice/题目 01.md", "# 题目")
        self.assertEqual(check(self.root), [])

    def test_missing_local_link_rejected(self):
        self.current()
        (self.root / "progress/practice/Q01.md").unlink()
        self.assertTrue(any("missing linked path" in error for error in check(self.root)))

    def test_duplicate_observation_rejected(self):
        self.current()
        self.write("progress/practice/Q01.md", "# Q01\n### Attempt A01\nFirst\n### Attempt A01\nRepeated")
        self.assertTrue(any("duplicate" in error for error in check(self.root)))

    def test_new_correction_preserves_old_observation(self):
        self.current()
        self.write("progress/practice/Q01.md", "# Q01\n### Attempt A01\nFirst\n### Correction C01\nCorrects A01")
        self.assertEqual(check(self.root), [])

    def test_capacity_mismatch_rejected(self):
        self.current()
        self.write("progress/progress.md", ENTRY.replace("Next task minutes: 5", "Next task minutes: 30"))
        self.assertTrue(any("exceeds" in error for error in check(self.root)))

    def test_negative_capacity_rejected(self):
        self.current()
        self.write("progress/progress.md", ENTRY.replace("Remaining minutes: 20", "Remaining minutes: -2"))
        self.assertTrue(any("negative" in error for error in check(self.root)))

    def test_unknown_capacity_is_not_invented(self):
        self.current()
        self.write("progress/progress.md", ENTRY.replace("Remaining minutes: 20", "Remaining minutes: unknown"))
        self.assertEqual(check(self.root), [])

    def test_preview_is_read_only(self):
        original = self.legacy()
        result = migrate(self.root, None, False)
        self.assertTrue(result[0].startswith("PREVIEW"))
        self.assertEqual(original, self.snapshot())

    def test_import_preserves_data_and_removes_active_json(self):
        original = self.legacy()
        artifact = {"course_id": "beam-course", "artifact_id": "beam-note",
                    "endpoint": {"statement": "反力满足平衡"}, "steps": [{"operation": "sum moments"}]}
        self.write("progress/artifacts/beam.compress.json", json.dumps(artifact, ensure_ascii=False))
        artifact_raw = (self.root / "progress/artifacts/beam.compress.json").read_bytes()
        result = migrate(self.root, None, True)
        self.assertTrue(result[0].startswith("IMPORTED"))
        self.assertEqual(check(self.root), [])
        self.assertEqual(list(self.root.rglob("*.json")), [])
        self.assertEqual(list(self.root.rglob("*.jsonl")), [])
        history = (self.root / "progress/history/imported-state.md").read_text(encoding="utf-8")
        for marker in ("独有标记-xyz", "看懂答案，并未独立作答", "Needed hint", "反力满足平衡", "sum moments"):
            self.assertIn(marker, history)
        entry = (self.root / "progress/progress.md").read_text(encoding="utf-8")
        self.assertIn("Answer exposure: unknown", entry)
        self.assertIn("resume gap", entry)
        self.assertNotIn("- Remaining minutes: 60", entry)
        with zipfile.ZipFile(self.root / "progress/history/legacy-backup.zip") as archive:
            for relative, raw in original.items():
                if relative.endswith((".json", ".jsonl")):
                    self.assertEqual(archive.read(relative), raw)
            self.assertEqual(archive.read("progress/artifacts/beam.compress.json"), artifact_raw)
        self.assertEqual((self.root / "reference/theory.md").read_bytes(), original["reference/theory.md"])

    def test_existing_markdown_refuses_overwrite(self):
        self.legacy()
        self.write("progress/progress.md", "User-owned existing state")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "already exists"):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_missing_source_is_explicit_gap(self):
        self.legacy()
        (self.root / "reference/theory.md").unlink()
        result = migrate(self.root, None, True)
        self.assertTrue(any("Missing legacy source" in line for line in result))
        self.assertEqual(check(self.root), [])

    def test_conflicting_duplicate_event_preserves_originals(self):
        self.legacy()
        conflict = copy.deepcopy(EVENT)
        conflict["result"]["level_observed"] = 3
        self.write("progress/event-conflict.json", json.dumps(conflict))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Conflicting duplicate"):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_outside_source_path_rejected(self):
        self.legacy()
        legacy = copy.deepcopy(LEGACY)
        legacy["source_materials"][0]["path"] = "../outside.md"
        self.write("progress/strategy.json", json.dumps(legacy))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "escapes"):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_malformed_input_preserves_originals(self):
        self.legacy()
        self.write("progress/mastery-evidence.jsonl", "{bad input")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_link_to_retired_json_blocks_import(self):
        self.legacy()
        self.write("progress/old-note.md", "[old state](strategy.json)")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "missing linked path"):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_partial_archival_failure_rolls_back_bytes(self):
        original = self.legacy()
        real_unlink = Path.unlink
        failed = False

        def fail_one(path, *args, **kwargs):
            nonlocal failed
            if path == self.root / "progress/mastery-evidence.jsonl" and not failed:
                failed = True
                raise OSError("simulated removal failure")
            return real_unlink(path, *args, **kwargs)

        with patch.object(Path, "unlink", fail_one):
            with self.assertRaisesRegex(OSError, "simulated"):
                migrate(self.root, None, True)
        self.assertTrue(failed)
        self.assertEqual(original, self.snapshot())

    def test_absolute_link_to_retired_json_blocks_import(self):
        self.legacy()
        absolute = (self.root / "progress/strategy.json").as_posix()
        self.write("progress/old.md", f"[old](<{absolute}>)")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "missing linked path"):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_reference_link_to_retired_json_blocks_import(self):
        self.legacy()
        self.write("progress/old.md", "[old][state]\n\n[state]: strategy.json")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "missing linked path"):
            migrate(self.root, None, True)
        self.assertEqual(before, self.snapshot())

    def test_undefined_reference_rejected(self):
        self.current()
        self.write("progress/practice/Q01.md", "[source][missing]")
        self.assertTrue(any("undefined link reference" in error for error in check(self.root)))

    def test_update_during_render_is_not_silently_archived(self):
        self.legacy()
        real_build = migrate_legacy.build

        def mutate_during_build(*args, **kwargs):
            result = real_build(*args, **kwargs)
            strategy = copy.deepcopy(LEGACY)
            strategy["latest_observation"] = "must not disappear from active state"
            self.write("progress/strategy.json", json.dumps(strategy))
            return result

        with patch.object(migrate_legacy, "build", mutate_during_build):
            with self.assertRaisesRegex(ValueError, "changed during migration"):
                migrate(self.root, None, True)
        current = json.loads((self.root / "progress/strategy.json").read_text(encoding="utf-8"))
        self.assertEqual(current["latest_observation"], "must not disappear from active state")
        self.assertFalse((self.root / "progress/progress.md").exists())
        self.assertFalse((self.root / "progress/history/legacy-backup.zip").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
