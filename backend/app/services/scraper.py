import requests
from recipe_scrapers import scrape_html

from app.dtos.dtos import ScrapedRecipeDto


HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def fetch_recipe_data(url: str) -> ScrapedRecipeDto:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
    )
    response.raise_for_status()

    scraper = scrape_html(
        html=response.text,
        org_url=url,
        wild_mode=True,
    )

    scraped_stuff: ScrapedRecipeDto = ScrapedRecipeDto(
        source_url=url,
        name=scraper.title(),
        ingredients=scraper.ingredients(),
        servings=scraper.yields(),
    )

    print("Scraped Stuff>>>>", scraped_stuff)

    return scraped_stuff