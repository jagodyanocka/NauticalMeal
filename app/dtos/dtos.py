from dataclasses import dataclass

@dataclass(frozen=True)
class ScrapedRecipeDto:
    source_url: str
    name: str
    servings: str | None
    ingredients: list[str]

