from app.dtos.dtos import PlannedMealDto
from app.services.scraper import fetch_recipe_data


def generate_shopping_list(
    meals: list[PlannedMealDto],
) -> str:
    recipes_data = []

    for meal in meals:
        recipe, _ = fetch_recipe_data(
            meal.recipe_url
        )

        recipes_data.append({
            "day": meal.day,
            "meal_type": meal.meal_type,
            "people": meal.people,
            "recipe": {
                "name": recipe.name,
                "servings": recipe.servings,
                "ingredients": [
                    ingredient.ingredient_name
                    for ingredient in recipe.ingredients.all()
                ],
            },
        })