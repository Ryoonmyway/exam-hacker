#!/usr/bin/env python3
"""Check a few concrete Markdown record invariants; never grade learning."""
from __future__ import annotations
import argparse
import re
import string
from pathlib import Path
from urllib.parse import unquote

SECTIONS = (
    ("目标与约束", "Goal and constraints"),
    ("掌握与优先级", "Mastery and priorities"),
    ("当前任务", "Current task"),
    ("下一步", "Next action"),
    ("最近更新", "Recent changes"),
)
LINK_START = re.compile(r"!?\[(?:\\.|[^\]\\\n])*\]\(")
REFERENCE = re.compile(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*", re.M)
REFERENCE_USE = re.compile(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]")
ATTEMPT = re.compile(r"^#{2,6}\s+(?:Attempt|Correction|作答|修正)\s+([\w.-]+)", re.M | re.I)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})([^\n]*)$")
ESCAPE = re.compile(r"\\([" + re.escape(string.punctuation) + r"])")


def mask(text: str) -> str:
    """Keep line boundaries so examples cannot join surrounding Markdown."""
    return re.sub(r"[^\n]", " ", text)


def without_code(text: str) -> str:
    """Mask fenced/indented blocks and matched backtick spans in record prose.

    This is a record checker, not a complete Markdown renderer. In particular,
    preserve ordinary indented paragraph/list continuations for link checking.
    """
    lines = []
    fence = None
    indented = False
    paragraph = False
    list_indent = 0
    for line in text.splitlines(keepends=True):
        expanded = line.expandtabs(4)
        content = expanded.rstrip("\r\n")
        if fence is not None:
            lines.append(mask(line))
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",}[ \t]*", content):
                fence = None
            continue
        opening = FENCE.match(content)
        if opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = opening[1]
            paragraph = False
            indented = False
            lines.append(mask(line))
            continue
        if not content.strip():
            lines.append(line)
            paragraph = False
            continue
        indent = len(content) - len(content.lstrip(" "))
        if indent >= list_indent + 4 and (indented or not paragraph):
            lines.append(mask(line))
            indented = True
            continue
        indented = False
        item = re.match(r"^ {0,3}(?:[-+*]|\d+[.)]) +", content)
        if item:
            list_indent = item.end()
        elif indent < list_indent:
            list_indent = 0
        lines.append(line)
        paragraph = not bool(re.match(r"^ {0,3}#{1,6}(?:\s|$)", content))

    # Inline spans belong to a prose block; unmatched ticks in separate blocks
    # must not hide intervening headings or real links.
    result = []
    paragraph_lines = []
    for line in lines:
        block_start = re.match(r"^ {0,3}(?:#{1,6}(?:\s|$)|[-+*] +|\d+[.)] +|>)", line)
        if not line.strip() or block_start:
            result.append(without_inline_code("".join(paragraph_lines)))
            paragraph_lines = []
        if not line.strip() or re.match(r"^ {0,3}#{1,6}(?:\s|$)", line):
            result.append(without_inline_code(line))
        else:
            paragraph_lines.append(line)
    result.append(without_inline_code("".join(paragraph_lines)))
    return "".join(result)


def without_inline_code(text: str) -> str:
    # Only an equal-length backtick run closes a span. Unmatched runs are prose.
    runs = list(re.finditer(r"`+", text))
    result = []
    end = 0
    index = 0
    while index < len(runs):
        start = runs[index]
        prefix = text[:start.start()]
        slashes = len(prefix) - len(prefix.rstrip("\\"))
        if slashes % 2:
            index += 1
            continue
        closing = next((j for j in range(index + 1, len(runs))
                        if len(runs[j][0]) == len(start[0])), None)
        if closing is None:
            index += 1
            continue
        stop = runs[closing].end()
        result.extend((text[end:start.start()], mask(text[start.start():stop])))
        end = stop
        index = closing + 1
    result.append(text[end:])
    return "".join(result)


def destination_at(text: str, start: int) -> tuple[str, int] | None:
    """Read one destination, retaining escapes until after URI handling."""
    pos = start
    angle = pos < len(text) and text[pos] == "<"
    if angle:
        pos += 1
        start = pos
    depth = 0
    while pos < len(text):
        char = text[pos]
        if char == "\\" and pos + 1 < len(text) and text[pos + 1] in string.punctuation:
            pos += 2
            continue
        if angle:
            if char == ">":
                return text[start:pos], pos + 1
            if char in "\n\r<":
                return None
        else:
            if char.isspace():
                break
            if char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
        pos += 1
    if angle or depth:
        return None
    return text[start:pos], pos


def inline_targets(text: str) -> list[str]:
    targets = []
    for match in LINK_START.finditer(text):
        start = match.end()
        while start < len(text) and text[start].isspace():
            start += 1
        parsed = destination_at(text, start)
        if parsed is None:
            continue
        target, pos = parsed
        before_space = pos
        while pos < len(text) and text[pos].isspace():
            pos += 1
        # Optional titles have their own delimiter, separate from the path.
        if pos > before_space and pos < len(text) and text[pos] in "\"'(":
            delimiter = ")" if text[pos] == "(" else text[pos]
            pos += 1
            while pos < len(text) and text[pos] != delimiter:
                if text[pos] == "\\" and pos + 1 < len(text) and text[pos + 1] in string.punctuation:
                    pos += 1
                pos += 1
            if pos == len(text):
                continue
            pos += 1
            while pos < len(text) and text[pos].isspace():
                pos += 1
        if pos < len(text) and text[pos] == ")":
            targets.append(target)
    return targets


def numeric_field(text: str, names: tuple[str, ...]) -> float | None:
    pattern = r"^\s*[-*]\s*(?:" + "|".join(map(re.escape, names)) + r")\s*[:：]\s*(-?\d+(?:\.\d+)?)\s*(?:minutes|分钟)?\s*$"
    match = re.search(pattern, text, re.M | re.I)
    return float(match.group(1)) if match else None


def check(root: Path, fallback_root: Path | None = None, removed: set[str] | None = None) -> list[str]:
    root = root.resolve()
    fallback_root = fallback_root.resolve() if fallback_root else None
    retired = {Path(relative) for relative in (removed or set())}
    errors: list[str] = []
    progress = root / "progress"
    entry = progress / "progress.md"
    if not entry.is_file():
        return ["Missing progress/progress.md"]
    body = without_code(entry.read_text(encoding="utf-8-sig"))
    headings = {m.casefold() for m in re.findall(r"^##\s+(.+?)\s*$", body, re.M)}
    for names in SECTIONS:
        if not any(name.casefold() in headings for name in names):
            errors.append("Missing progress section: " + " / ".join(names))
    remaining = numeric_field(body, ("剩余分钟", "Remaining minutes"))
    next_minutes = numeric_field(body, ("下一任务分钟", "Next task minutes"))
    if any(value is not None and value < 0 for value in (remaining, next_minutes)):
        errors.append("Capacity and task duration cannot be negative")
    if remaining is not None and next_minutes is not None and next_minutes > remaining:
        errors.append(f"Next task ({next_minutes:g} min) exceeds remaining capacity ({remaining:g} min)")
    for path in sorted(progress.rglob("*.md")):
        text = without_code(path.read_text(encoding="utf-8-sig"))
        relative = path.relative_to(root)
        if "history" not in path.relative_to(progress).parts:
            ids = ATTEMPT.findall(text)
            if len(ids) != len(set(ids)):
                errors.append(f"{relative}: duplicate attempt/correction ID")
        definitions = {}
        for match in REFERENCE.finditer(text):
            parsed = destination_at(text, match.end())
            if parsed is not None:
                definitions[" ".join(match[1].split()).casefold()] = parsed[0]
        for usage in REFERENCE_USE.finditer(text):
            label = " ".join((usage.group(2) or usage.group(1)).split()).casefold()
            if label not in definitions:
                errors.append(f"{relative}: undefined link reference {label}")
        targets = inline_targets(text) + list(definitions.values())
        for raw_target in targets:
            target = ESCAPE.sub(r"\1", raw_target)
            if target.startswith(("#", "http:", "https:", "mailto:", "data:", "codex:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            destination = Path(target)
            if not destination.is_absolute():
                destination = path.parent / destination
            destination = destination.resolve()
            fallback_exists = False
            relative_target = None
            if destination.is_relative_to(root):
                relative_target = destination.relative_to(root)
            elif fallback_root is not None and destination.is_relative_to(fallback_root):
                relative_target = destination.relative_to(fallback_root)
                destination = root / relative_target
            if relative_target in retired:
                errors.append(f"{relative}: missing linked path after migration {target}")
                continue
            if fallback_root is not None and relative_target is not None:
                fallback_exists = (fallback_root / relative_target).exists()
            if not destination.exists() and not fallback_exists:
                errors.append(f"{relative}: missing linked path {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("course_root", type=Path)
    args = parser.parse_args()
    try:
        errors = check(args.course_root.resolve())
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    if errors:
        print("\n".join("ERROR: " + error for error in errors))
        return 1
    print("PASS: Markdown entry, local links, attempt IDs, and explicit next-task capacity.")
    print("Not checked: teaching quality, source truth, mathematics, or mastery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
