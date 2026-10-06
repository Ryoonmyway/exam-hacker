#!/usr/bin/env python3
"""Preview or import one legacy Exam Hacker course into Markdown."""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from check_learning_record import check


def inside(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"Path escapes course root: {path}")
    return resolved


def read_snapshot(path: Path, snapshots: dict[Path, bytes]) -> bytes:
    if path not in snapshots:
        snapshots[path] = path.read_bytes()
    return snapshots[path]


def load(path: Path, snapshots: dict[Path, bytes]):
    return json.loads(read_snapshot(path, snapshots).decode("utf-8-sig"))


def value_text(value) -> str:
    if value is None:
        return "unknown (legacy null)"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("\r\n", "\n").replace("\r", "\n")


def render_tree(value, depth: int = 0) -> list[str]:
    """Preserve every leaf, including unfamiliar fields, in readable Markdown."""
    indent = "  " * depth
    if isinstance(value, dict):
        if not value:
            return [indent + "- (empty mapping)"]
        result = []
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                result += [f"{indent}- **{key}**:"] + render_tree(child, depth + 1)
            else:
                result.append(f"{indent}- **{key}**: " + value_text(child).replace("\n", "\n" + indent + "  "))
        return result
    if isinstance(value, list):
        if not value:
            return [indent + "- (empty list)"]
        result = []
        for index, child in enumerate(value, 1):
            result += [f"{indent}- Item {index}:"] + render_tree(child, depth + 1)
        return result
    return [indent + "- " + value_text(value).replace("\n", "\n" + indent + "  ")]


def code(value) -> str:
    return "`" + value_text(value).replace("`", "'").replace("\n", " / ") + "`"


def rel_link(from_path: str, to_path: str, label: str) -> str:
    rel = os.path.relpath(to_path, str(Path(from_path).parent)).replace("\\", "/")
    return f"[{label}](<{rel}>)"


def collect(root: Path, strategy_path: Path):
    snapshots: dict[Path, bytes] = {}
    strategy = load(strategy_path, snapshots)
    if not isinstance(strategy, dict) or not isinstance(strategy.get("course"), dict):
        raise ValueError("Unsupported legacy strategy: missing course object")
    if not isinstance(strategy.get("action_list"), list):
        raise ValueError("Unsupported legacy strategy: missing action_list")
    inputs = {strategy_path: strategy}
    course_id = strategy["course"].get("id")
    for pattern in ("progress/strategy-r*.json", "progress/history/strategy-r*.json"):
        for path in sorted(root.glob(pattern)):
            path = inside(root, path)
            data = load(path, snapshots)
            if not isinstance(data, dict) or data.get("course", {}).get("id") != course_id:
                raise ValueError(f"Historical strategy course mismatch: {path}")
            inputs[path] = data
    event_candidates = []
    log = root / "progress/mastery-evidence.jsonl"
    if log.exists():
        log = inside(root, log)
        events = [json.loads(line) for line in read_snapshot(log, snapshots).decode("utf-8-sig").splitlines() if line.strip()]
        inputs[log] = events
        event_candidates.extend(events)
    for path in sorted(root.glob("progress/event-*.json")):
        path = inside(root, path)
        event = load(path, snapshots)
        inputs[path] = event
        event_candidates.append(event)
    events_by_id = {}
    for event in event_candidates:
        if not isinstance(event, dict):
            raise ValueError("Legacy evidence event is not an object")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", event_id):
            raise ValueError("Legacy evidence event lacks a safe stable ID")
        if event.get("course_id") != course_id:
            raise ValueError(f"Evidence belongs to another course: {event_id}")
        if event_id in events_by_id and events_by_id[event_id] != event:
            raise ValueError(f"Conflicting duplicate event: {event_id}")
        events_by_id[event_id] = event
    artifacts = []
    for pattern in ("progress/artifacts/*.compress.json", "progress/artifacts/*.solve.json"):
        for path in sorted(root.glob(pattern)):
            path = inside(root, path)
            artifact = load(path, snapshots)
            if not isinstance(artifact, dict) or artifact.get("course_id") != course_id:
                raise ValueError(f"Artifact course mismatch: {path}")
            inputs[path] = artifact
            artifacts.append(artifact)
    return strategy, inputs, list(events_by_id.values()), artifacts, snapshots


def build(root: Path, strategy: dict, inputs: dict, events: list, artifacts: list):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    warnings = ["Legacy planned Sessions do not prove a pending question or known answer exposure.",
                "Legacy source verification labels are imported, not independently reverified.",
                "Legacy available minutes may be stale; confirm before treating them as remaining capacity."]
    history = ["# Imported legacy history", "", "Historical snapshot only; current decisions live in ../progress.md.", ""]
    for path, value in inputs.items():
        history += ["## " + path.relative_to(root).as_posix(), ""]
        history += render_tree(value) + [""]
    materials = ["# Materials", "", "Imported source claims; inspect relevant content before making new source-backed judgments.", ""]
    for source in strategy.get("source_materials", []):
        materials += ["## " + str(source.get("id", "unknown")), ""]
        raw_path = source.get("path")
        if raw_path:
            source_path = inside(root, root / raw_path)
            if source_path.exists():
                materials += ["- Source: " + rel_link("progress/materials.md", raw_path, str(source.get("label", raw_path)))]
            else:
                warning = f"Missing legacy source: {raw_path}"
                warnings.append(warning)
                materials += ["- Gap: " + warning]
        materials += render_tree(source) + [""]
    materials += ["## Recorded gaps", ""] + render_tree(strategy.get("material_gaps", []))
    evidence = ["# Imported observations", "", "Conditions and evidence types are retained; import itself proves no mastery.", ""]
    for event in events:
        evidence += ["### Attempt " + event["event_id"], ""] + render_tree(event) + [""]
    if not events:
        evidence += ["No legacy observed events were found. Self-reports remain in the progress snapshot.", ""]
    entry_path = "progress/progress.md"
    history_link = rel_link(entry_path, "progress/history/imported-state.md", "complete historical fields")
    evidence_link = rel_link(entry_path, "progress/practice/imported-evidence.md", "imported observations")
    course = strategy["course"]
    planning = strategy.get("planning_context", {})
    availability = planning.get("availability", {})
    entry = [
        "# " + str(course.get("name", course.get("id", "Exam review"))), "",
        "## Goal and constraints", "",
        "- Course ID: " + code(course.get("id")),
        "- Target: " + code(course.get("target_score")),
        "- Exam date: " + code(planning.get("exam_date")),
        "- Timezone: " + code(planning.get("timezone")),
        "- Legacy available minutes (not reconfirmed remaining): " + code(availability.get("total_minutes")),
        "- Source index: [materials](materials.md)",
        "- Prior decisions and source details: " + history_link, "",
        "## Mastery and priorities", "",
        "Imported ability claims (retain their evidence types and conditions):", "",
    ]
    for item in strategy.get("mastery_snapshot", []):
        entry += ["### " + str(item.get("topic_id", "unknown")), ""] + render_tree(item) + [""]
    entry += ["Observation details: " + evidence_link, "",
              "Legacy priorities (re-evaluate P0/P1/P2 from the current goal; do not map mechanically):", ""]
    for priority in strategy.get("priorities", []):
        entry += ["- " + str(priority.get("title", priority.get("id", "unknown"))) +
                  ": " + str(priority.get("level", "unknown")) + " — " + str(priority.get("reason", ""))]
    entry += ["", "## Current task", "",
              "- Stage: resume gap; no exact pending question is established by this import.",
              "- Answer exposure: unknown.",
              "- Do not infer an unanswered task from an active/queued Session label.", ""]
    next_ids = strategy.get("loop_state", {}).get("next_session_ids", [])
    selected = [s for s in strategy["action_list"] if s.get("id") in next_ids]
    for session in selected:
        entry += ["### Legacy planned task " + str(session.get("id")), ""] + render_tree(session) + [""]
    entry += ["## Next action", "",
              "Recover any actual unfinished question and its exposure state from the learner or existing notes. "
              "If no pending question exists, verify present constraints and present a suitable new task. "
              "Do not ask the learner to choose a specialist.", "",
              "## Recent changes", "",
              f"- {now}: Imported legacy files once into Markdown; see {history_link}.",
              "- Recovery backup: [legacy input ZIP](history/legacy-backup.zip)", "",
              "## Import warnings", ""] + ["- " + warning for warning in warnings]
    if artifacts:
        entry += ["", "## Existing learning artifacts", ""]
        for artifact in artifacts:
            display = artifact.get("display_path")
            if display:
                path = inside(root, root / display)
                if path.is_file():
                    entry += ["- " + rel_link(entry_path, display, str(artifact.get("artifact_id", display)))]
                    continue
            entry += ["- " + code(artifact.get("artifact_id")) + ": full imported content in " + history_link]
    return {
        "progress/progress.md": "\n".join(entry) + "\n",
        "progress/materials.md": "\n".join(materials) + "\n",
        "progress/practice/imported-evidence.md": "\n".join(evidence) + "\n",
        "progress/history/imported-state.md": "\n".join(history) + "\n",
    }, warnings


def migrate(root: Path, strategy_relative: str | None, apply: bool) -> list[str]:
    root = root.resolve(strict=True)
    candidates = [root / strategy_relative] if strategy_relative else [
        root / "progress/strategy.json", root / "strategy.json"]
    strategy_path = next((inside(root, p) for p in candidates if p.is_file()), None)
    if strategy_path is None:
        raise ValueError("No canonical legacy strategy; select a known snapshot with --strategy")
    if (root / "progress/progress.md").exists():
        raise ValueError("Markdown entry already exists; reconcile instead of overwriting")
    strategy, inputs, events, artifacts, originals = collect(root, strategy_path)
    outputs, warnings = build(root, strategy, inputs, events, artifacts)
    archive_rel = "progress/history/legacy-backup.zip"
    for relative in [*outputs, archive_rel]:
        target = inside(root, root / relative)
        if target.exists():
            raise ValueError(f"Refusing to overwrite: {relative}")
    if not apply:
        return ["PREVIEW: no files changed", *("Import: " + p.relative_to(root).as_posix() for p in inputs),
                *("Create: " + p for p in outputs), "Backup: " + archive_rel,
                *("WARNING: " + w for w in warnings)]
    created = []
    with tempfile.TemporaryDirectory(prefix="exam-hacker-import-") as temp:
        candidate = Path(temp)
        # Copy only Markdown, never a potentially large PDF/course corpus.
        for existing in (root / "progress").rglob("*.md"):
            existing = inside(root, existing)
            target = candidate / existing.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(existing.read_bytes())
        for relative, content in outputs.items():
            target = candidate / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
        archive = candidate / archive_rel
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as backup:
            for path, raw in originals.items():
                backup.writestr(path.relative_to(root).as_posix(), raw)
        with zipfile.ZipFile(archive) as backup:
            for path, raw in originals.items():
                if backup.read(path.relative_to(root).as_posix()) != raw:
                    raise ValueError(f"Backup verification failed: {path}")
        errors = check(candidate, root, {p.relative_to(root).as_posix() for p in inputs})
        if errors:
            raise ValueError("Candidate validation failed: " + "; ".join(errors))
        for path, raw in originals.items():
            if path.read_bytes() != raw:
                raise ValueError(f"Legacy input changed during migration: {path}")
        try:
            # Backup goes first; entry goes last. Recheck destinations to avoid clobbering.
            for relative in [archive_rel, *(p for p in outputs if p != "progress/progress.md"), "progress/progress.md"]:
                target = inside(root, root / relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as handle:
                    created.append(target)
                    handle.write((candidate / relative).read_bytes())
            for path, raw in originals.items():
                if path.read_bytes() != raw:
                    raise ValueError(f"Legacy input changed before archival: {path}")
            for path in originals:
                inside(root, path).unlink()
        except Exception:
            # Restore byte-identical inputs, then remove only outputs created by this run.
            for path, raw in originals.items():
                if not path.exists():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(raw)
            for path in reversed(created):
                inside(root, path).unlink(missing_ok=True)
            raise
    return ["IMPORTED: Markdown is now authoritative; legacy bytes preserved in " + archive_rel,
            *("WARNING: " + w for w in warnings)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_root", type=Path)
    parser.add_argument("--strategy", help="Known legacy strategy path relative to course root")
    parser.add_argument("--apply", action="store_true", help="Apply after preview; default is read-only")
    args = parser.parse_args()
    try:
        print("\n".join(migrate(args.course_root, args.strategy, args.apply)))
        return 0
    except (OSError, ValueError, TypeError, KeyError, zipfile.BadZipFile) as exc:
        print(f"ERROR: migration stopped: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
