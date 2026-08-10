from dataclasses import dataclass

@dataclass(frozen=True)
class ScrapedRecipeDto:
    source_url: str
    name: str
    servings: str | None
    ingredients: list[str]

@dataclass(frozen=True)
class PlannedMealDto:
    day: int
    meal_type: str
    recipe_url: str
    people: int

@dataclass(frozen=True)
class ShoppingListDto:
    meals: list[PlannedMealDto]