#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_PATH = ROOT / "RECIPE_BOOK.md"
INDEX_PATH = ROOT / "RECIPE_INDEX.md"

WEEKLY_SECTION = "7-Day Meal Flow Shopping List (Auto-Generated)"
PANTRY_SECTION = "Pantry and All-Recipes Staples (Auto-Generated)"
FLOW_SECTION = "7-Day Low-Carb Meal Flow (Optional)"

ALIAS_TO_TITLE = {
    "egg muffins": "Spinach Feta Egg Muffins",
    "greek chicken salad": "Greek Chicken Salad Bowls",
    "salmon + asparagus": "Garlic Butter Salmon with Asparagus",
    "leftover salmon salad": "Garlic Butter Salmon with Asparagus",
    "cauliflower fried rice": "Cauliflower Fried Rice",
    "tuscan chicken": "Creamy Tuscan Chicken",
    "greek salad bowl": "Greek Chicken Salad Bowls",
    "sausage + veggies": "Sheet Pan Sausage and Veggies",
    "zoodle bolognese": "Zucchini Noodle Turkey Bolognese",
    "broccoli cheddar soup": "Broccoli Cheddar Soup (Low-Carb)",
    "soup + side salad": "Broccoli Cheddar Soup (Low-Carb)",
    "soup": "Broccoli Cheddar Soup (Low-Carb)",
    "chia pudding": "Chia Vanilla Pudding",
    "greek yogurt bowl": "Greek Yogurt Bowl with Walnuts and Cinnamon",
    "taco peppers": "Taco Stuffed Bell Peppers",
    "lemon-basil yogurt sauce": "Lemon-Basil Yogurt Sauce",
    "smoky tomato-oregano sauce": "Smoky Tomato-Oregano Sauce",
    "viral cottage cheese flatbread wrap": "Viral Cottage Cheese Flatbread Wrap",
}

CATEGORY_KEYWORDS = {
    "Proteins": [
        "chicken",
        "turkey",
        "beef",
        "salmon",
        "sausage",
        "shrimp",
        "protein powder",
        "collagen",
        "egg",
    ],
    "Produce": [
        "spinach",
        "romaine",
        "zucchini",
        "broccoli",
        "asparagus",
        "pepper",
        "onion",
        "garlic",
        "cucumber",
        "tomato",
        "lemon",
        "basil",
        "green onion",
        "strawberr",
    ],
    "Dairy": [
        "yogurt",
        "feta",
        "cheddar",
        "parmesan",
        "cream",
        "butter",
        "cottage cheese",
    ],
}

CATEGORY_OVERRIDES = {
    "avocado oil": "Pantry",
    "chicken broth": "Pantry",
    "coconut aminos": "Pantry",
    "olive oil": "Pantry",
    "peanut butter": "Pantry",
    "sesame oil": "Pantry",
    "san marzano tomatoes": "Pantry",
}

INGREDIENT_KEYWORDS = [
    "sugar-free maple syrup",
    "san marzano tomatoes",
    "sun-dried tomatoes",
    "cherry tomatoes",
    "cauliflower rice",
    "chicken breast",
    "chicken thighs",
    "smoked sausage",
    "ground turkey",
    "ground beef",
    "coconut aminos",
    "soy sauce",
    "avocado oil",
    "sesame oil",
    "olive oil",
    "almond flour",
    "peanut butter",
    "protein powder",
    "monk fruit sweetener",
    "almond milk",
    "chicken broth",
    "cottage cheese",
    "greek yogurt",
    "heavy cream",
    "parmesan",
    "cheddar",
    "feta",
    "butter",
    "salmon",
    "asparagus",
    "spinach",
    "romaine",
    "cucumber",
    "olives",
    "lemon juice",
    "lemon",
    "oregano",
    "garlic",
    "zucchini",
    "italian seasoning",
    "green onions",
    "peas",
    "carrots",
    "eggs",
    "bell peppers",
    "taco seasoning",
    "salsa",
    "broccoli",
    "onion",
    "chia seeds",
    "walnuts",
    "cinnamon",
    "fresh basil",
    "smoked paprika",
    "chili flakes",
]


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in re.finditer(r"(?ms)^## (.+?)\n(.*?)(?=^## |\Z)", text):
        sections[match.group(1).strip()] = match.group(2).strip()
    return sections


def parse_recipe_paths(index_text: str) -> list[Path]:
    paths: list[Path] = []
    for line in index_text.splitlines():
        m = re.search(r"\((recipes/[^)]+\.md)\)", line)
        if m:
            paths.append(ROOT / m.group(1))
    return paths


def recipe_title(path: Path) -> str:
    first = path.read_text(encoding="utf-8").splitlines()[0].strip()
    return first.removeprefix("# ").strip()


def extract_ingredients(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    out: list[str] = []
    in_ing = False
    for line in text.splitlines():
        if line.startswith("### Ingredients"):
            in_ing = True
            continue
        if in_ing and line.startswith("### "):
            break
        if in_ing and line.startswith("- "):
            out.extend(extract_keywords(line[2:].strip()))
    return out


def extract_keywords(item: str) -> list[str]:
    item = item.lower()
    if "optional" in item:
        return []
    item = re.sub(r"\(.*?\)", "", item)
    found: list[str] = []
    for key in INGREDIENT_KEYWORDS:
        if key in item:
            found.append(key)
    return found


def categorize(items: set[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for item in sorted(items):
        if item in CATEGORY_OVERRIDES:
            buckets[CATEGORY_OVERRIDES[item]].append(item)
            continue
        placed = False
        for cat, keys in CATEGORY_KEYWORDS.items():
            if any(k in item for k in keys):
                buckets[cat].append(item)
                placed = True
                break
        if not placed:
            buckets["Pantry"].append(item)
    return buckets


def parse_week_flow(flow_text: str) -> set[str]:
    found: set[str] = set()
    text = flow_text.lower()
    for alias, title in sorted(ALIAS_TO_TITLE.items(), key=lambda kv: len(kv[0]), reverse=True):
        if alias in text:
            found.add(title)
    return found


def replace_section(text: str, title: str, new_body: str) -> str:
    pattern = rf"(?ms)^## {re.escape(title)}\n.*?(?=^## |\Z)"
    replacement = f"## {title}\n{new_body.strip()}\n\n"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text)
    return text.rstrip() + f"\n\n{replacement}"


def main() -> None:
    book_text = BOOK_PATH.read_text(encoding="utf-8")
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    sections = parse_sections(book_text)
    recipe_paths = parse_recipe_paths(index_text)

    title_to_path = {recipe_title(p): p for p in recipe_paths}
    weekly_titles = parse_week_flow(sections.get(FLOW_SECTION, ""))

    weekly_items: set[str] = set()
    for t in weekly_titles:
        p = title_to_path.get(t)
        if p:
            weekly_items.update(extract_ingredients(p))

    all_items: set[str] = set()
    for p in recipe_paths:
        all_items.update(extract_ingredients(p))

    weekly_buckets = categorize(weekly_items)
    pantry_buckets = categorize(all_items)
    order = ["Proteins", "Produce", "Dairy", "Pantry"]

    weekly_body_lines = ["- Generated from recipes referenced in the current 7-day meal flow."]
    for cat in order:
        vals = weekly_buckets.get(cat, [])
        if vals:
            weekly_body_lines.append(f"- **{cat}:** {', '.join(vals)}")

    pantry_body_lines = ["- Generated from ingredients across all recipes in `recipes/`."]
    for cat in order:
        vals = pantry_buckets.get(cat, [])
        if vals:
            pantry_body_lines.append(f"- **{cat}:** {', '.join(vals)}")

    weekly_body = "\n".join(weekly_body_lines)
    pantry_body = "\n".join(pantry_body_lines)

    updated = replace_section(book_text, WEEKLY_SECTION, weekly_body)
    updated = replace_section(updated, PANTRY_SECTION, pantry_body)
    BOOK_PATH.write_text(updated.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
