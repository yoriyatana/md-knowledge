#!/usr/bin/env python3
"""Batch-format Markdown files while preserving their wording."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


ATX_HEADING = re.compile(r"^(?P<indent>\s{0,3})(?P<marks>#{1,6})\s*(?P<text>.*?)(?:\s+#+\s*)?$")
LIST_ITEM = re.compile(r"^(?P<indent>\s*)(?P<marker>[-+*]|\d+[.)])\s*(?P<text>.*)$")


def iter_markdown_files(root: Path) -> Iterable[Path]:
    yield from sorted(path for path in root.rglob("*.md") if path.is_file())


def format_markdown(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    formatted: list[str] = []
    blank_pending = False

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            blank_pending = True
            continue

        if blank_pending and formatted:
            formatted.append("")
        blank_pending = False

        heading = ATX_HEADING.match(line)
        if heading and heading.group("text"):
            line = f"{heading.group('indent')}{heading.group('marks')} {heading.group('text').strip()}"
        else:
            list_item = LIST_ITEM.match(line)
            if list_item and list_item.group("text"):
                line = (
                    f"{list_item.group('indent')}{list_item.group('marker')} "
                    f"{list_item.group('text').strip()}"
                )
        formatted.append(line)

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
    args = parser.parse_args()

    if not args.input.is_dir():
        parser.error(f"input directory does not exist: {args.input}")

    results = []
    for source in iter_markdown_files(args.input):
        relative = source.relative_to(args.input)
        results.append(process_file(source, args.output / relative))

    report = {
        "input": str(args.input),
        "output": str(args.output),
        "files": results,
        "summary": {
            "total": len(results),
            "changed": sum(bool(item["changed"]) for item in results),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Processed {len(results)} Markdown file(s); {report['summary']['changed']} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
