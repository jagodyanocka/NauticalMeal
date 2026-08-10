from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)

    source_url = models.URLField(
        max_length=2000,
        unique=True
    )

    servings = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    raw_text = models.TextField()

    def __str__(self) -> str:
        return self.raw_text

