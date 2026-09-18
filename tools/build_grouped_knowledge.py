#!/usr/bin/env python3
"""Build deterministic grouped Markdown documents from an approved manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any


IMAGE_LINK = re.compile(r"(!\[[^\]]*\])\(([^)]+)\)")


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_files(root: Path, group: dict[str, Any]) -> list[Path]:
    if "sources" in group:
        return [root / item for item in group["sources"]]
    prefix = group["source_prefix"]
    return sorted(root.glob(f"{prefix}*.md"))


def validate(manifest: dict[str, Any], root: Path) -> list[str]:
    errors = []
    seen: set[str] = set()
    for group in manifest["groups"]:
        if group["id"] in seen:
            errors.append(f"duplicate group id: {group['id']}")
        seen.add(group["id"])
        for source in source_files(root, group):
            if not source.is_file():
                errors.append(f"missing source: {source}")
    return errors


def copy_images(text: str, source: Path, destination: Path, output_root: Path) -> str:
    asset_dir = output_root / "assets" / destination.stem
    asset_dir.mkdir(parents=True, exist_ok=True)

    def replace(match: re.Match[str]) -> str:
        target = match.group(2).split()[0].strip("<>")
        image = (source.parent / target).resolve()
        if not image.is_file():
            return match.group(0)
        digest = hashlib.sha1(str(image).encode("utf-8")).hexdigest()[:10]
        asset_name = f"{digest}-{image.name}"
        shutil.copy2(image, asset_dir / asset_name)
        relative = Path(
            os.path.relpath(asset_dir / asset_name, destination.parent)
        )
        return f"{match.group(1)}({relative.as_posix()})"

    return IMAGE_LINK.sub(replace, text)


def dedupe_blocks(text: str, seen: set[str]) -> str:
    blocks = re.split(r"\n{2,}", text)
    kept = []
    for block in blocks:
        key = re.sub(r"\s+", " ", block).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        kept.append(block.strip())
    return "\n\n".join(kept)


def build_consolidate(group: dict[str, Any], root: Path, output_root: Path) -> list[str]:
    destination = output_root / group["path"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    sections = [f"# {group['topic']}\n\n> Generated deterministically from the approved grouping manifest.\n"]
    sources = source_files(root, group)
    for source in sources:
        text = source.read_text(encoding="utf-8", errors="replace")
        text = copy_images(text, source, destination, output_root)
        sections.append(f"## Source: `{source.as_posix()}`\n\n{dedupe_blocks(text, seen)}")
    destination.write_text("\n\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return [source.as_posix() for source in sources]


def build_index(group: dict[str, Any], root: Path, output_root: Path) -> list[str]:
    destination = output_root / group["path"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    sources = source_files(root, group)
    lines = [
        f"# {group['topic']}",
        "",
        "| Topic | Type | Platform/Vendor | Source | Related document |",
        "|---|---|---|---|---|",
    ]
    related = ""
    for source in sources:
        relative = source.relative_to(root).as_posix()
        lines.append(f"| {source.stem} | {group['kind']} | {group['platform']} | `{relative}` | {related} |")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [source.as_posix() for source in sources]


def build_index_root(manifest: dict[str, Any], output_root: Path) -> None:
    lines = ["# Grouped Knowledge", "", "Deterministic output generated from `reports/grouping-manifest.json`.", ""]
    for group in manifest["groups"]:
        lines.append(f"- [{group['topic']}]({group['path']}) — {group['kind']} — {group['platform']}")
    (output_root / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "build"))
    parser.add_argument("--manifest", type=Path, default=Path("reports/grouping-manifest.json"))
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    source_root = args.source_root or Path(manifest["source_root"])
    output_root = args.output_root or Path(manifest["output_root"])
    errors = validate(manifest, source_root)
    if errors:
        raise SystemExit("\n".join(errors))
    if args.command == "plan":
        for group in manifest["groups"]:
            count = len(source_files(source_root, group))
            print(f"{group['id']}: {group['type']} ({count} source(s)) -> {group['path']}")
        return 0
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    mapping = {}
    for group in manifest["groups"]:
        sources = (
            build_consolidate(group, source_root, output_root)
            if group["type"] == "consolidate"
            else build_index(group, source_root, output_root)
        )
        mapping[group["id"]] = {"output": group["path"], "sources": sources, "type": group["type"]}
    build_index_root(manifest, output_root)
    (output_root / "source-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(mapping)} grouped entries in {output_root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
