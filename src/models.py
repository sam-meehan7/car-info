from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class CarData(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[float] = None
    mileage: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    engine_size: Optional[str] = None
    color: Optional[str] = None
    location: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "make": "Audi",
                "model": "A4",
                "year": 2020,
                "price": 35000,
                "mileage": "45,000 km",
                "fuel_type": "Diesel",
                "transmission": "Automatic",
                "engine_size": "2.0L",
                "color": "Black",
                "location": "Dublin",
            }
        }


class ScrapeRequest(BaseModel):
    url: HttpUrl

    class Config:
        json_schema_extra = {
            "example": {"url": "https://www.carzone.ie/used-cars/audi/a4/fpa/4170857"}
        }


class BatchScrapeRequest(BaseModel):
    urls: List[HttpUrl]

    class Config:
        json_schema_extra = {
            "example": {
                "urls": [
                    "https://www.carzone.ie/used-cars/audi/a4/fpa/4170857",
                    "https://www.carzone.ie/used-cars/bmw/3-series/fpa/4170858",
                ]
            }
        }
