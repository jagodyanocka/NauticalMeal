from ninja import Router

from app.api.schemas.schemas import GenerateShoppingListSchema
from app.dtos.dtos import PlannedMealDto
from app.services.shopping_list_service import generate_shopping_list

router = Router()

@router.post("/generate")
def generate_shopping_list_endpoint(
    request,
    payload: GenerateShoppingListSchema,
):
    meals = [
        PlannedMealDto(
            day=meal.day,
            meal_type=meal.meal_type,
            recipe_url=meal.recipe_url,
            people=meal.people,
        )
        for meal in payload.meals
    ]

    return generate_shopping_list(meals)