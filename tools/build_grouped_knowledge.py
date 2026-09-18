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
    if "source_prefix" in group:
        return sorted(root.glob(f"{group['source_prefix']}*.md"))
    directories = group.get("source_directories", [])
    return sorted(
        path
        for directory in directories
        for path in (root / directory).glob("*.md")
    )


def group_type(group: dict[str, Any]) -> str:
    return group.get("type", group.get("action", ""))


def path_part(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value or "general"


def group_path(group: dict[str, Any]) -> str:
    if all(group.get(field) for field in ("vendor", "level2_doctype", "level1_domain", "level3_feature")):
        return "/".join(
            [
                path_part(group["vendor"]),
                path_part(group["level2_doctype"]),
                path_part(group["level1_domain"]),
                f"{path_part(group['level3_feature'])}.md",
            ]
        )
    return group.get("path", group.get("destination", ""))


def validate(manifest: dict[str, Any], root: Path) -> list[str]:
    errors = []
    seen: set[str] = set()
    for group in manifest["groups"]:
        if group["id"] in seen:
            errors.append(f"duplicate group id: {group['id']}")
        seen.add(group["id"])
        if manifest.get("version") == 3:
            for field in ("vendor", "level2_doctype", "level1_domain", "level3_feature"):
                if not group.get(field):
                    errors.append(f"missing v3 field {field}: {group['id']}")
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
    destination = output_root / group_path(group)
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
    destination = output_root / group_path(group)
    destination.parent.mkdir(parents=True, exist_ok=True)
    sources = source_files(root, group)
    lines = [
        f"# {group['topic']}",
        "",
        "| Topic | Type | Platform/Vendor | Source | Related document |",
        "|---|---|---|---|---|",
    ]
    related = ""
    kind = group.get("kind", group.get("level2_doctype", "Index"))
    platform = group.get("platform", "Mixed")
    for source in sources:
        relative = source.relative_to(root).as_posix()
        lines.append(f"| {source.stem} | {kind} | {platform} | `{relative}` | {related} |")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [source.as_posix() for source in sources]


def build_index_root(manifest: dict[str, Any], output_root: Path) -> None:
    entries = {
        group_path(group): group
        for group in manifest["groups"]
    }
    tree: dict[str, dict[str, Any]] = {}
    for path in entries:
        node = tree
        parts = Path(path).parts
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault(parts[-1], None)

    lines = [
        "# Grouped Knowledge",
        "",
        "Deterministic output generated from `reports/grouping-manifest.json`.",
        "",
    ]

    def render(node: dict[str, Any], prefix: str = "") -> None:
        for name in sorted(node):
            child = node[name]
            if child is None:
                path = name if not prefix else f"{prefix}/{name}"
                group = entries[path]
                kind = group.get("kind", group.get("level2_doctype", ""))
                platform = group.get("platform", "Mixed")
                lines.append(
                    f"{'  ' * (len(Path(path).parts) - 1)}- "
                    f"[{group['topic']}]({path}) — {kind} — {platform}"
                )
            else:
                path = name if not prefix else f"{prefix}/{name}"
                lines.append(f"{'  ' * len(Path(path).parts[:-1])}- **{name}/**")
                render(child, path)

    render(tree)
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
            print(f"{group['id']}: {group_type(group)} ({count} source(s)) -> {group_path(group)}")
        return 0
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    mapping = {}
    for group in manifest["groups"]:
        sources = (
            build_consolidate(group, source_root, output_root)
            if group_type(group) == "consolidate"
            else build_index(group, source_root, output_root)
        )
        mapping[group["id"]] = {
            "output": group_path(group),
            "sources": sources,
            "type": group_type(group),
            "vendor": group.get("vendor"),
            "domain": group.get("level1_domain"),
            "feature": group.get("level3_feature"),
            "doctype": group.get("level2_doctype"),
        }
    build_index_root(manifest, output_root)
    (output_root / "source-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(mapping)} grouped entries in {output_root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
