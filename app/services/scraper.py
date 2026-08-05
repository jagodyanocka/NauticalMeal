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

    html = response.text

    try:
        scraper = scrape_html(
            html=html,
            org_url=url,
        )
    except Exception:
        # Fallback for unknown sites containing Schema.org Recipe data.
        scraper = scrape_html(
            html=html,
            org_url=url,
            wild_mode=True,
        )
    scraped = ScrapedRecipeDto(
        source_url=url,
        name=scraper.title(),
        ingredients=scraper.ingredients(),
        servings=scraper.yields(),
    )

    print(scraped)
    return scraped
