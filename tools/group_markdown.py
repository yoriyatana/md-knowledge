#!/usr/bin/env python3
"""Propose local semantic Markdown groups and build reviewed topic documents with Gemini."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_WRITING_MODEL = "gemini-2.5-flash"


def markdown_files(root: Path, excluded: set[str]) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if path.is_file() and not any(part in excluded for part in path.relative_to(root).parts)
    )


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedding_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return f"FILE: {path.name}\n{text[:12000]}"


def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def load_cache(path: Path) -> dict[str, list[float]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def propose(args: argparse.Namespace) -> None:
    model = SentenceTransformer(args.embedding_model)
    files = markdown_files(args.input, set(args.exclude_dir))
    cache = load_cache(args.cache)
    texts: list[str] = []
    pending: list[tuple[Path, str]] = []
    for path in files:
        digest = content_hash(path)
        key = f"{path}:{digest}"
        if key not in cache:
            pending.append((path, key))
        texts.append(key)

    for start in range(0, len(pending), args.batch_size):
        batch = pending[start : start + args.batch_size]
        vectors = model.encode(
            [embedding_text(path) for path, _ in batch],
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        for vector, (_, key) in zip(vectors, batch):
            cache[key] = vector.tolist()
    args.cache.parent.mkdir(parents=True, exist_ok=True)
    args.cache.write_text(json.dumps(cache), encoding="utf-8")

    groups: list[list[int]] = []
    assigned: set[int] = set()
    vectors = [cache[f"{path}:{content_hash(path)}"] for path in files]
    for index, vector in enumerate(vectors):
        if index in assigned:
            continue
        group = [index]
        assigned.add(index)
        for candidate in range(index + 1, len(vectors)):
            if cosine(vector, vectors[candidate]) >= args.threshold:
                group.append(candidate)
                assigned.add(candidate)
        groups.append(group)

    output = {
        "input": str(args.input),
        "embedding_model": args.embedding_model,
        "threshold": args.threshold,
        "review_required": True,
        "groups": [
            {
                "id": f"group-{index + 1:04d}",
                "approved": False,
                "files": [str(files[item]) for item in group],
            }
            for index, group in enumerate(groups)
            if len(group) > 1
        ],
        "ungrouped": [str(files[index]) for index in range(len(files)) if index not in {item for group in groups if len(group) > 1 for item in group}],
    }
    args.proposals.parent.mkdir(parents=True, exist_ok=True)
    args.proposals.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(output['groups'])} proposed group(s); review {args.proposals}.")


def image_inputs(source: Path) -> list[types.Part]:
    inputs: list[types.Part] = []
    pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for target in pattern.findall(source.read_text(encoding="utf-8", errors="replace")):
        image = (source.parent / target.split()[0].strip("<>")).resolve()
        if image.suffix.lower() not in IMAGE_EXTENSIONS or not image.is_file():
            continue
        mime = "image/jpeg" if image.suffix.lower() in {".jpg", ".jpeg"} else f"image/{image.suffix.lower().lstrip('.')}"
        inputs.append(types.Part.from_bytes(data=image.read_bytes(), mime_type=mime))
    return inputs


def build(args: argparse.Namespace) -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit("GEMINI_API_KEY is required for build; do not store it in the repository.")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    proposals = json.loads(args.proposals.read_text(encoding="utf-8"))
    approved = [group for group in proposals["groups"] if group.get("approved") is True]
    if not approved:
        raise SystemExit("No approved groups found. Set approved=true in the proposal JSON first.")

    for group in approved:
        source_paths = [Path(item) for item in group["files"]]
        source_text = "\n\n".join(
            f"--- SOURCE: {path} ---\n{path.read_text(encoding='utf-8', errors='replace')}"
            for path in source_paths
        )
        prompt = (
            "Write a coherent Markdown knowledge article from the supplied source notes. "
            "Preserve the source language and technical terms. Do not invent facts. "
            "Include a short summary, organized sections, practical details, and a "
            "Sources section listing every source path. When an image is supplied, "
            "describe useful text or diagrams from it under an 'Image notes' subsection "
            "and keep the image embedded after the description."
        )
        content: list[types.Part] = [types.Part.from_text(text=prompt + "\n\n" + source_text)]
        for path in source_paths:
            content.extend(image_inputs(path))
        response = client.models.generate_content(
            model=args.writing_model,
            contents=types.Content(role="user", parts=content),
        )
        destination = args.output / f"{group['id']}.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        document = (response.text or "").strip()
        image_lines: list[str] = []
        image_dir = args.output / "assets" / group["id"]
        for source in source_paths:
            for target in re.findall(
                r"!\[[^\]]*\]\(([^)]+)\)",
                source.read_text(encoding="utf-8", errors="replace"),
            ):
                image = (source.parent / target.split()[0].strip("<>")).resolve()
                if image.suffix.lower() not in IMAGE_EXTENSIONS or not image.is_file():
                    continue
                asset_name = f"{source.stem[:40]}-{image.name}"
                asset = image_dir / asset_name
                asset.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(image, asset)
                image_lines.append(f"- `{source}`: ![{image.name}](assets/{group['id']}/{asset_name})")
        if image_lines:
            document += "\n\n## Source images\n\n" + "\n".join(image_lines)
        document += "\n"
        destination.write_text(document, encoding="utf-8")
    print(f"Built {len(approved)} grouped document(s) in {args.output}.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    propose_parser = subparsers.add_parser("propose")
    propose_parser.add_argument("--input", type=Path, default=Path("formatted"))
    propose_parser.add_argument("--proposals", type=Path, default=Path("reports/group-proposals.json"))
    propose_parser.add_argument("--cache", type=Path, default=Path(".cache/embeddings.json"))
    propose_parser.add_argument("--threshold", type=float, default=0.82)
    propose_parser.add_argument("--batch-size", type=int, default=32)
    propose_parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    propose_parser.add_argument("--exclude-dir", action="append", default=["Login_Credentials"])
    propose_parser.set_defaults(function=propose)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--proposals", type=Path, default=Path("reports/group-proposals.json"))
    build_parser.add_argument("--output", type=Path, default=Path("grouped"))
    build_parser.add_argument("--writing-model", default=DEFAULT_WRITING_MODEL)
    build_parser.set_defaults(function=build)

    args = parser.parse_args()
    args.function(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
