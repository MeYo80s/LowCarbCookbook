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
- `templates/recipe-template.md` - copy/paste template for new recipes

## Recommended Workflow
1. Add or edit a recipe in `recipes/...`.
2. Update `RECIPE_INDEX.md` when adding a new recipe file.
3. Regenerate `RECIPE_BOOK.md` from individual recipes:
   - `python3 scripts/generate_recipe_book.py`
4. Refresh shopping lists:
   - `python3 scripts/update_shopping_lists.py`
5. Keep `RECIPE_BOOK.md` as your shareable master copy.
