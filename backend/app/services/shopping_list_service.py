import re

from app.ai.schemas import ShoppingList, ShoppingListIngredient
from app.dtos.dtos import PlannedMealDto
from app.services.ollama_client import get_ai_result
from app.services.scraper import fetch_recipe_data

# Mixed fractions ("1 1/2"), fractions ("1/2"), decimals ("2,5" / "2.5"), integers.
_NUMBER_PATTERN = re.compile(r"\d+\s+\d+/\d+|\d+/\d+|\d+(?:[.,]\d+)?")


def _extract_servings(servings: str | None) -> float | None:
    """'4 portins' / 'Serves 4' -> 4.0"""
    if not servings:
        return None
    match = _NUMBER_PATTERN.search(servings)
    if not match:
        return None
    return float(match.group().replace(",", "."))


def _scale_ingredient_line(line: str, scale: float) -> str:
    """Multiply every number in an ingredient line by scale."""

    def scale_match(match: re.Match[str]) -> str:
        text = match.group()
        if "/" in text:
            parts = text.split()
            numerator, denominator = parts[-1].split("/")
            value = float(numerator) / float(denominator)
            if len(parts) == 2:
                value += float(parts[0])
        else:
            value = float(text.replace(",", "."))

        scaled = round(value * scale, 2)
        if scaled == int(scaled):
            return str(int(scaled))
        result = f"{scaled:g}"
        if "," in text:
            result = result.replace(".", ",")
        return result

    return _NUMBER_PATTERN.sub(scale_match, line)


def generate_shopping_list(
    meals: list[PlannedMealDto],
) -> ShoppingList:
    shopping_list_data = []

    for meal in meals:
        recipe = fetch_recipe_data(meal.recipe_url)
        shopping_list_data.extend(recipe.ingredients)

    return get_ai_result(shopping_list_data)

