#!/usr/bin/env python3
"""List the installed Exam Hacker specialists and reject ambiguous copies."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SPECIALISTS = (
    "exam-hacker-triage",
    "exam-hacker-compress",
    "exam-hacker-solve",
    "exam-hacker-drill",
    "exam-hacker-replan",
)


def frontmatter_name(skill_file: Path) -> str | None:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.removeprefix("name:").strip().strip('"\'') or None
    return None


def default_roots() -> list[Path]:
    home = Path.home()
    return [home / ".codex" / "skills", home / ".agents" / "skills"]


def inspect(roots: list[Path]) -> dict[str, object]:
    installed: list[dict[str, str]] = []
    missing: list[str] = []
    malformed: list[dict[str, str]] = []
    conflicts: list[dict[str, object]] = []

    for name in SPECIALISTS:
        candidates: list[Path] = []
        for root in roots:
            candidate = root / name
            if (candidate / "SKILL.md").is_file():
                candidates.append(candidate)

        if not candidates:
            missing.append(name)
            continue

        if len(candidates) > 1:
            conflicts.append(
                {
                    "name": name,
                    "paths": [str(path) for path in candidates],
                    "reason": "duplicate-installation",
                }
            )
            continue

        candidate = candidates[0]
        skill_file = candidate / "SKILL.md"
        try:
            declared_name = frontmatter_name(skill_file)
        except (OSError, UnicodeError) as exc:
            reason = "invalid UTF-8" if isinstance(exc, UnicodeError) else "unreadable SKILL.md"
            malformed.append({"name": name, "path": str(candidate),
                              "declared_name": "", "reason": f"{reason}: {exc}"})
            continue
        if declared_name != name:
            malformed.append(
                {
                    "name": name,
                    "path": str(candidate),
                    "declared_name": declared_name or "",
                }
            )
            continue

        installed.append(
            {
                "name": name,
                "path": str(candidate),
                "resolved_path": str(candidate.resolve()),
            }
        )

    return {
        "complete": not missing and not malformed and not conflicts,
        "search_roots": [str(root) for root in roots],
        "installed": installed,
        "missing": missing,
        "malformed": malformed,
        "conflicts": conflicts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List installed Exam Hacker specialists"
    )
    parser.add_argument(
        "--search-root",
        action="append",
        type=Path,
        help="Override an installation root; repeat for multiple roots",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when the installation is incomplete or ambiguous",
    )
    args = parser.parse_args()

    roots = args.search_root or default_roots()
    result = inspect(roots)
    for root in result["search_roots"]:
        print(f"Search root: {root}")
    for item in result["installed"]:
        print(f"AVAILABLE: {item['name']} -> {item['resolved_path']}")
    for name in result["missing"]:
        print(f"MISSING: {name}")
    for item in result["malformed"]:
        reason = item.get("reason", "missing or mismatched frontmatter name")
        print(f"MALFORMED: {item['name']} at {item['path']}: {reason}")
    for item in result["conflicts"]:
        print(f"CONFLICT: {item['name']}: {', '.join(item['paths'])}")
    if args.strict and not result["complete"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
