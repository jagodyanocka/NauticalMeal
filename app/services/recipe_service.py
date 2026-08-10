from django.db import transaction

from app.models.models import Recipe, RecipeIngredient
from app.services.scraper import fetch_recipe_data


@transaction.atomic
def create_recipe_from_url(url: str) -> tuple[Recipe, bool]:
    existing_recipe = Recipe.objects.filter(
        source_url=url,
    ).first()

    if existing_recipe:
        return existing_recipe, False

    scraped = fetch_recipe_data(url)

    recipe = Recipe.objects.create(
        name=scraped.name,
        source_url=scraped.source_url,
        servings=scraped.servings,
    )

    RecipeIngredient.objects.bulk_create(
        [
            RecipeIngredient(
                recipe=recipe,
                raw_text=ingredient,
            )
            for ingredient in scraped.ingredients
        ]
    )

    return recipe, True
