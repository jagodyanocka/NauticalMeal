from pydantic import BaseModel


class ShoppingListIngredient(BaseModel):
    name: str
    quantity_to_buy: str


class ShoppingList(BaseModel):
    ingredients: list[ShoppingListIngredient]

