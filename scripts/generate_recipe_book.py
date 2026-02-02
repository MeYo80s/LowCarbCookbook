#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "RECIPE_BOOK.md"
INDEX_PATH = ROOT / "RECIPE_INDEX.md"


KEEP_SECTIONS = [
    "How to Use This Book",
    "Macro Key",
    "Sauce Pairing Guide",
    "7-Day Low-Carb Meal Flow (Optional)",
    "7-Day Meal Flow Shopping List (Auto-Generated)",
    "Pantry and All-Recipes Staples (Auto-Generated)",
]


def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def parse_sections(markdown: str) -> dict[str, str]:
    parts = re.split(r"(?m)^## ", markdown)
    out: dict[str, str] = {}
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        out[title] = body
    return out


def parse_recipe_titles_from_book(book_text: str) -> list[str]:
    return re.findall(r"(?m)^## \d+\)\s+(.+)$", book_text)


def parse_recipe_paths(index_text: str) -> list[Path]:
    paths: list[Path] = []
    for line in index_text.splitlines():
        match = re.search(r"\((recipes/[^)]+\.md)\)", line)
        if match:
            paths.append(ROOT / match.group(1))
    return paths


def parse_recipe_file(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8").strip()
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"Recipe missing title heading: {path}")
    title = lines[0][2:].strip()
    body = "\n".join(lines[1:]).strip()
    return title, body


def build_toc(recipe_titles: list[str]) -> list[str]:
    lines = [
        "## Table of Contents",
        "- [How to Use This Book](#how-to-use-this-book)",
        "- [Macro Key](#macro-key)",
    ]
    for i, title in enumerate(recipe_titles, start=1):
        lines.append(f"- [{i}) {title}](#{i}-{slugify(title)})")
    lines.extend(
        [
            "- [Sauce Pairing Guide](#sauce-pairing-guide)",
            "- [7-Day Low-Carb Meal Flow (Optional)](#7-day-low-carb-meal-flow-optional)",
            "- [7-Day Meal Flow Shopping List (Auto-Generated)](#7-day-meal-flow-shopping-list-auto-generated)",
            "- [Pantry and All-Recipes Staples (Auto-Generated)](#pantry-and-all-recipes-staples-auto-generated)",
        ]
    )
    return lines


def main() -> None:
    book_text = BOOK_PATH.read_text(encoding="utf-8")
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    sections = parse_sections(book_text)

    book_title = re.search(r"(?m)^# .+$", book_text)
    subtitle = re.search(r"(?m)^Created for .+$", book_text)
    if not book_title or not subtitle:
        raise ValueError("Could not find book title/subtitle in RECIPE_BOOK.md")

    index_paths = parse_recipe_paths(index_text)
    path_by_title = {}
    for path in index_paths:
        recipe_title, _ = parse_recipe_file(path)
        path_by_title[recipe_title] = path

    ordered_paths: list[Path] = []
    for title_from_book in parse_recipe_titles_from_book(book_text):
        path = path_by_title.get(title_from_book)
        if path:
            ordered_paths.append(path)

    # Add any new indexed recipes not yet present in the book.
    for path in index_paths:
        if path not in ordered_paths:
            ordered_paths.append(path)

    recipes = [parse_recipe_file(path) for path in ordered_paths]
    recipe_titles = [t for t, _ in recipes]

    lines: list[str] = [book_title.group(0), "", subtitle.group(0), ""]
    lines.extend(build_toc(recipe_titles))

    for section_name in KEEP_SECTIONS[:2]:
        section_body = sections.get(section_name, "")
        lines.extend(["", f"## {section_name}", section_body, "", "---"])

    for i, (recipe_title, recipe_body) in enumerate(recipes, start=1):
        lines.extend(["", f"## {i}) {recipe_title}", recipe_body, "", "---"])

    for section_name in KEEP_SECTIONS[2:]:
        section_body = sections.get(section_name, "")
        lines.extend(["", f"## {section_name}", section_body, "", "---"])

    if lines[-1] == "---":
        lines.pop()

    BOOK_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
