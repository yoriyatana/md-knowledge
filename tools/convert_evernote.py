#!/usr/bin/env python3
"""Convert Evernote ENEX exports to Markdown and extracted resources."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from markdownify import markdownify


NOTEBOOK_DIRS = {
    "AJSPR-v19A": Path("classification/Concepts_Theory/AJSPR-v19A"),
    "2022_FTEL-PS": Path("2022_FTEL-PS"),
    "JTAC Descriptions": Path("JTAC_Descriptions"),
    "Outlook Tips & Tricks": Path("Outlook"),
}
SKIP_NOTEBOOKS = {"Login Credentials"}
SAFE_NAME = re.compile(r"[^\w.\-+(),#|= \u0080-\uffff]+", re.UNICODE)


def safe_name(value: str, fallback: str) -> str:
    value = SAFE_NAME.sub("_", value.strip()).strip(" .")
    return value or fallback


def notebook_dir(path: Path) -> Path:
    return NOTEBOOK_DIRS.get(path.stem, Path(safe_name(path.stem, "Notebook").replace(" ", "_")))


def resource_filename(resource: ET.Element, digest: str, mime: str) -> str:
    attrs = resource.find("resource-attributes")
    original = attrs.findtext("file-name", "") if attrs is not None else ""
    suffix = Path(original).suffix if original else {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/gif": ".gif",
        "image/svg+xml": ".svg",
        "application/pdf": ".pdf",
    }.get(mime, "")
    return f"{digest}{suffix}"


def convert_content(content: str, resources: dict[str, str]) -> str:
    content = html.unescape(content)
    content = re.sub(r"^\s*<\?xml[^>]*\?>", "", content, count=1, flags=re.IGNORECASE)
    content = re.sub(
        r'<en-media\b[^>]*\bhash="([^"]+)"[^>]*/?>',
        lambda m: f'<img src="evernote-resource://{m.group(1)}" />',
        content,
        flags=re.IGNORECASE,
    )
    soup = BeautifulSoup(content, "html.parser")
    for image in soup.find_all("img"):
        source = image.get("src", "")
        if source.startswith("evernote-resource://"):
            digest = source.rsplit("/", 1)[-1]
            image["src"] = resources.get(digest, source)
    text = markdownify(str(soup), heading_style="ATX", bullets="-")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n" if text.strip() else ""


def convert_notebook(source: Path, output: Path) -> dict[str, Any]:
    root = ET.parse(source).getroot()
    notes = root.findall("note")
    destination = output / notebook_dir(source)
    destination.mkdir(parents=True, exist_ok=True)
    used: set[str] = set()
    results = []
    for index, note in enumerate(notes, start=1):
        title = note.findtext("title", "").strip() or f"Untitled_Note_{index}"
        stem = safe_name(title, f"Untitled_Note_{index}")
        candidate = stem
        suffix = 2
        while candidate in used or (destination / f"{candidate}.md").exists():
            candidate = f"{stem}_{suffix}"
            suffix += 1
        used.add(candidate)

        asset_dir = destination / "image"
        resource_paths: dict[str, str] = {}
        for resource in note.findall("resource"):
            digest = resource.findtext("data", "").strip()
            if not digest:
                continue
            raw = base64.b64decode(re.sub(r"\s+", "", digest))
            resource_hash = resource.findtext("resource-attributes")  # keeps parsing explicit
            del resource_hash
            digest_key = resource.get("hash") or hashlib.md5(raw).hexdigest()
            mime = resource.findtext("mime", "") or "application/octet-stream"
            filename = resource_filename(resource, digest_key, mime)
            asset_dir.mkdir(parents=True, exist_ok=True)
            asset_path = asset_dir / filename
            asset_path.write_bytes(raw)
            resource_paths[digest_key] = f"image/{filename}"

        content = convert_content(note.findtext("content", ""), resource_paths)
        destination_file = destination / f"{candidate}.md"
        destination_file.write_text(f"# {title}\n\n{content}", encoding="utf-8")
        results.append({
            "title": title,
            "destination": str(destination_file),
            "resources": len(resource_paths),
            "content_chars": len(content),
        })
    return {"source": str(source), "notes": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("raw_evernote"))
    parser.add_argument("--output", type=Path, default=Path("raw_evernote_converted"))
    parser.add_argument("--report", type=Path, default=Path("reports/evernote-conversion-report.json"))
    args = parser.parse_args()
    if not args.input.is_dir():
        parser.error(f"input directory does not exist: {args.input}")
    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)
    reports = []
    skipped = []
    for source in sorted(args.input.glob("*.enex")):
        if source.stem in SKIP_NOTEBOOKS:
            skipped.append(source.name)
            continue
        reports.append(convert_notebook(source, args.output))
    report = {
        "input": str(args.input),
        "output": str(args.output),
        "skipped_notebooks": skipped,
        "notebooks": reports,
        "summary": {
            "notebooks": len(reports),
            "notes": sum(len(item["notes"]) for item in reports),
            "resources": sum(note["resources"] for item in reports for note in item["notes"]),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
