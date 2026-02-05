# LowCarbCookbook

A simple, practical low-carb recipe collection with estimated net carbs, a 7-day meal flow, and a shopping list.

## What's In This Repo
- `RECIPE_BOOK.md` - the full recipe book
- `RECIPE_INDEX.md` - category index for individual recipe files

## Recipe Highlights
- 15 low-carb recipes across breakfast, mains, soups, sauces, and snacks
- Estimated net carbs per serving
- Estimated macros per serving
- 7-day meal flow for easy planning
- Auto-generated weekly and all-recipes shopping lists

## How to Use
1. Open `RECIPE_BOOK.md`.
2. Pick recipes for the week (or follow the 7-day meal flow).
3. Use the shopping list section to plan groceries.

## Website View (GitHub Pages)
- After enabling GitHub Pages for this repo, share:
  - `https://meyo80s.github.io/LowCarbCookbook/`
- In GitHub: `Settings` -> `Pages` -> `Build and deployment`
  - `Source`: `Deploy from a branch`
  - `Branch`: `main` and `/ (root)`

## Notes
- Net carbs are estimates and can vary by ingredient brands.
- Check labels for hidden sugars in sauces and packaged foods.

## Contributing
Want to add recipes? Open a pull request with:
- Recipe name
- Ingredients
- Instructions
- Estimated net carbs per serving

## Repo Structure
- `RECIPE_BOOK.md` - full cookbook in one file
- `RECIPE_INDEX.md` - quick links to individual recipe files
- `recipes/` - categorized recipe files (`breakfast`, `mains`, `soups`, `sauces`, `snacks`)
- `assets/recipes/` - optional recipe photos
- `templates/recipe-template.md` - copy/paste template for new recipes

## Optional Recipe Photos
- Add images to `assets/recipes/` using slug-style names.
- In recipe files, use image paths like `../../assets/recipes/recipe-name.jpg`.
- If a recipe has no photo, just remove the image line in the template.

## Recommended Workflow
1. Add or edit a recipe in `recipes/...`.
2. Update `RECIPE_INDEX.md` when adding a new recipe file.
3. Choose your week in `weekly_plan.json` (recipe titles must match index titles).
4. Generate your 7-day menu:
   - `python3 scripts/generate_weekly_plan.py`
5. Regenerate `RECIPE_BOOK.md` from individual recipes:
   - `python3 scripts/generate_recipe_book.py`
6. Refresh shopping lists:
   - `python3 scripts/update_shopping_lists.py`
7. Keep `RECIPE_BOOK.md` as your shareable master copy.
