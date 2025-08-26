import httpx
from typing import Optional, List
from models import CarData
from config import settings


class FirecrawlScraper:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {settings.firecrawl_api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        self.api_url = settings.firecrawl_api_url

    async def scrape_car(self, url: str) -> Optional[CarData]:
        """
        Scrape a car listing and return only the CarData.
        Returns None if scraping fails.
        """

        # Define the schema for car data extraction
        car_schema = {
            "type": "object",
            "required": [],
            "properties": {
                "make": {"type": "string"},
                "model": {"type": "string"},
                "year": {"type": "integer"},
                "price": {"type": "number"},
                "mileage": {"type": "string"},
                "fuel_type": {"type": "string"},
                "transmission": {"type": "string"},
                "engine_size": {"type": "string"},
                "color": {"type": "string"},
                "location": {"type": "string"},
            },
        }

        payload = {
            "url": str(url),
            "onlyMainContent": True,
            "formats": [{"type": "json", "schema": car_schema}],
        }

        try:
            response = await self.client.post(self.api_url, json=payload)
            response.raise_for_status()

            data = response.json()
            json_data = data.get("data", {}).get("json", {})

            if json_data:
                return CarData(**json_data)
            return None

        except Exception:
            return None

    async def scrape_multiple(self, urls: List[str]) -> List[Optional[CarData]]:
        """Scrape multiple URLs and return list of CarData (None for failed scrapes)."""
        import asyncio

        tasks = [self.scrape_car(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global scraper instance
scraper = FirecrawlScraper()
