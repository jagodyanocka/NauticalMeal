from ninja import Schema


class PlannedMealSchema(Schema):
    day: int
    meal_type: str
    recipe_url: str
    people: int


class GenerateShoppingListSchema(Schema):
    meals: list[PlannedMealSchema]