#!/usr/bin/env python3
"""Batch-format Markdown files while preserving their wording."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Iterable


ATX_HEADING = re.compile(r"^(?P<indent>\s{0,3})(?P<marks>#{1,6})\s*(?P<text>.*?)(?:\s+#+\s*)?$")
LIST_ITEM = re.compile(r"^(?P<indent>\s*)(?P<marker>[-+*]|\d+[.)])\s*(?P<text>.*)$")
COMMAND = re.compile(
    r"^(?:"
    r"(?:[\w.-]+@[\w.-]+[>#%]|root@[\w.-]+[>#%]|%|>)\s*"
    r"|(?:show|set|delete|deactivate|activate|request|clear|restart|monitor|"
    r"test|commit|configure|display|load|rollback|file|run|sysctl|grep|tail|"
    r"less|more|scp|ssh|cat|ping|traceroute|tcpdump|wireshark)\b"
    r")",
    re.IGNORECASE,
)
FENCE = re.compile(r"^\s*(```|~~~)")
OUTPUT_LINE = re.compile(
    r"^(?:"
    r".*\b(?:not enabled|not supported|viol|error|failed)\b"
    r"|(?:[\w\\.-]+:\s*[-\d]|Packet types\b|group\s+|pppoe\s+)"
    r"|.*\b(?:Received|Dropped|Rate|State|counts)\b.*"
    r")",
    re.IGNORECASE,
)


def iter_markdown_files(root: Path, excluded_dirs: set[str]) -> Iterable[Path]:
    yield from sorted(
        path
        for path in root.rglob("*.md")
        if path.is_file() and not any(part in excluded_dirs for part in path.relative_to(root).parts)
    )


def iter_assets(root: Path, excluded_dirs: set[str]) -> Iterable[Path]:
    yield from sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() not in {".md", ".markdown"}
        and path.name != ".DS_Store"
        and not any(part in excluded_dirs for part in path.relative_to(root).parts)
    )


def format_markdown(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    formatted: list[str] = []
    blank_pending = False
    in_fence = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if not paragraph:
            return
        normalized = [item.rstrip() for item in paragraph]
        command_items = [
            LIST_ITEM.match(item).group("text").strip()
            if LIST_ITEM.match(item)
            else item.strip()
            for item in normalized
        ]
        is_command_block = any(
            COMMAND.match(item) or OUTPUT_LINE.match(item) for item in command_items
        )
        if is_command_block and not any(
            item.startswith(("!", "|", "#")) or "![" in item for item in normalized
        ):
            if formatted and formatted[-1] != "":
                formatted.append("")
            formatted.extend(["```text", *command_items, "```"])
        else:
            formatted.extend(normalized)
        paragraph = []

    for raw_line in lines:
        line = raw_line.rstrip()
        if FENCE.match(line):
            flush_paragraph()
            in_fence = not in_fence
            formatted.append(line)
            blank_pending = False
            continue
        if in_fence:
            formatted.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            blank_pending = True
            continue

        if blank_pending and formatted and formatted[-1] != "":
            formatted.append("")
        blank_pending = False

        heading = ATX_HEADING.match(line)
        if heading and heading.group("text"):
            line = f"{heading.group('indent')}{heading.group('marks')} {heading.group('text').strip()}"
        if heading and heading.group("text"):
            flush_paragraph()
            formatted.append(line)
            continue
        else:
            list_item = LIST_ITEM.match(line)
            if list_item and list_item.group("text"):
                line = (
                    f"{list_item.group('indent')}{list_item.group('marker')} "
                    f"{list_item.group('text').strip()}"
                )
        paragraph.append(line)

    flush_paragraph()
    return "\n".join(formatted).strip() + "\n" if formatted else ""


def process_file(source: Path, destination: Path) -> dict[str, object]:
    original = source.read_text(encoding="utf-8", errors="replace")
    formatted = format_markdown(original)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(formatted, encoding="utf-8")
    return {
        "source": str(source),
        "destination": str(destination),
        "changed": original != formatted,
        "input_bytes": len(original.encode("utf-8")),
        "output_bytes": len(formatted.encode("utf-8")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("raw"))
    parser.add_argument("--output", type=Path, default=Path("formatted"))
    parser.add_argument("--report", type=Path, default=Path("reports/reformat-report.json"))
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="directory name to exclude recursively; may be repeated",
    )
    args = parser.parse_args()

    if not args.input.is_dir():
        parser.error(f"input directory does not exist: {args.input}")

    results = []
    excluded_dirs = set(args.exclude_dir)
    for source in iter_markdown_files(args.input, excluded_dirs):
        relative = source.relative_to(args.input)
        results.append(process_file(source, args.output / relative))

    assets = []
    for source in iter_assets(args.input, excluded_dirs):
        relative = source.relative_to(args.input)
        destination = args.output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        assets.append(
            {
                "source": str(source),
                "destination": str(destination),
                "bytes": source.stat().st_size,
            }
        )

    report = {
        "input": str(args.input),
        "output": str(args.output),
        "files": results,
        "assets": assets,
        "summary": {
            "total": len(results),
            "changed": sum(bool(item["changed"]) for item in results),
            "assets": len(assets),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Processed {len(results)} Markdown file(s); {report['summary']['changed']} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
