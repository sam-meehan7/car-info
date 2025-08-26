from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
import uvicorn

from config import settings
from scraper import scraper
from models import CarData, ScrapeRequest, BatchScrapeRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    yield
    await scraper.close()


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API for scraping car data from listings",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scrape", response_model=Optional[CarData])
async def scrape_single(request: ScrapeRequest):
    """
    Scrape a single car listing and return the car data.
    Returns null if scraping fails.
    """
    result = await scraper.scrape_car(str(request.url))

    if result is None:
        raise HTTPException(status_code=422, detail="Failed to scrape the provided URL")

    return result


@app.post("/scrape/batch", response_model=List[Optional[CarData]])
async def scrape_batch(request: BatchScrapeRequest):
    """
    Scrape multiple car listings and return a list of car data.
    Failed scrapes will be null in the list.
    """
    results = await scraper.scrape_multiple([str(url) for url in request.urls])
    return results


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
