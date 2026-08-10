from ninja import Router

from app.api.schemas.schemas import GenerateShoppingListSchema
from app.dtos.dtos import PlannedMealDto

router = Router()

@router.post("/generate")
def generate_shopping_list(request, payload: GenerateShoppingListSchema):
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