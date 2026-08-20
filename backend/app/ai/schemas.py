from pydantic import BaseModel


class ShoppingListIngredient(BaseModel):
    name: str
    quantity: str
    servings: str
    people: int

class ShoppingList(BaseModel):
    ingredients: list[ShoppingListIngredient]

class ListWithScale(BaseModel):
    ingredients: list[ShoppingListIngredient]
