#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "RECIPE_BOOK.md"
INDEX_PATH = ROOT / "RECIPE_INDEX.md"
PLAN_PATH = ROOT / "weekly_plan.json"
FLOW_SECTION = "7-Day Low-Carb Meal Flow (Optional)"


def parse_recipe_paths(index_text: str) -> list[Path]:
    paths: list[Path] = []
    for line in index_text.splitlines():
        match = re.search(r"\((recipes/[^)]+\.md)\)", line)
        if match:
            paths.append(ROOT / match.group(1))
    return paths


def recipe_title(path: Path) -> str:
    first_line = path.read_text(encoding="utf-8").splitlines()[0].strip()
    return first_line.removeprefix("# ").strip()


def replace_section(text: str, section_title: str, body: str) -> str:
    pattern = rf"(?ms)^## {re.escape(section_title)}\n.*?(?=^## |\Z)"
    replacement = f"## {section_title}\n{body.strip()}\n\n"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text)
    return text.rstrip() + f"\n\n{replacement}"


def main() -> None:
    if not PLAN_PATH.exists():
        raise FileNotFoundError("weekly_plan.json is missing.")

    index_text = INDEX_PATH.read_text(encoding="utf-8")
    recipe_paths = parse_recipe_paths(index_text)
    known_titles = {recipe_title(path) for path in recipe_paths}

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    days = plan.get("days", [])
    if not isinstance(days, list) or not days:
        raise ValueError("weekly_plan.json must include a non-empty 'days' list.")

    flow_lines: list[str] = []
    for item in days:
        day = item.get("day")
        recipes = item.get("recipes", [])
        if not day or not isinstance(recipes, list) or not recipes:
            raise ValueError("Each day needs 'day' and non-empty 'recipes'.")
        unknown = [title for title in recipes if title not in known_titles]
        if unknown:
            raise ValueError(f"Unknown recipe title(s) in {day}: {', '.join(unknown)}")
        flow_lines.append(f"- **{day}:** {' / '.join(recipes)}")

    book_text = BOOK_PATH.read_text(encoding="utf-8")
    updated = replace_section(book_text, FLOW_SECTION, "\n".join(flow_lines))
    BOOK_PATH.write_text(updated.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
