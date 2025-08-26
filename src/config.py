from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    api_title: str = "Car Scraper API"
    api_version: str = "1.0.0"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Firecrawl Configuration
    firecrawl_api_key: str
    firecrawl_api_url: str = "https://api.firecrawl.dev/v2/scrape"

    class Config:
        env_file = ".env"


settings = Settings()
