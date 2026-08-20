from app.ai.schemas import ShoppingList, ListWithScale
from app.dtos.dtos import PlannedMealDto
from app.services.llm_client import get_ai_result
from app.services.scraper import fetch_recipe_data

def generate_shopping_list(
    meals: list[PlannedMealDto],
) -> ListWithScale | None:
    shopping_list_data = []

    for meal in meals:
        recipe = fetch_recipe_data(meal.recipe_url)
        people = meal.people
        for ingredient in recipe.ingredients:
            shopping_list_data.append(
                {
                    "ingredient": ingredient,
                    "servings": recipe.servings if recipe.servings is not None else "1",
                    "people": people,
                }
            )
    print("PEOPLE???", shopping_list_data)
    shopping_list_with_servings = get_ai_result(shopping_list_data)

    return shopping_list_with_servings

