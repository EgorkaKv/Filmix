from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    MOVIE = "MOVIE"
    SERIES = "SERIES"

class MovieBase(BaseModel):
    title: str
    original_title: Optional[str] = None
    original_language: Optional[str] = None
    series_name: Optional[str] = None  # Для группировки (например "Шрек")
    year: int
    director: str
    genres: List[str]
    rating: Optional[float] = None  # Рейтинг (например, IMDb)
    my_rating: Optional[int] = Field(None, ge=1, le=100)  # Твоя оценка от 1 до 100
    watch_date: Optional[datetime] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    content_type: ContentType = ContentType.MOVIE

class MovieCreate(MovieBase):
    """Модель для создания нового фильма/сериала"""
    pass

class MovieUpdate(BaseModel):
    """Модель для обновления фильма/сериала"""
    title: Optional[str] = None
    original_title: Optional[str] = None
    original_language: Optional[str] = None
    series_name: Optional[str] = None
    year: Optional[int] = None
    director: Optional[str] = None
    genres: Optional[List[str]] = None
    rating: Optional[float] = None
    my_rating: Optional[int] = Field(None, ge=1, le=100)
    watch_date: Optional[datetime] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    content_type: Optional[ContentType] = None

class Movie(MovieBase):
    """Полная модель фильма/сериала с ID"""
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "689751511bb87333c3fe855a",
                "title": "District 13",
                "original_title": "District 13",
                "original_language": "fr",
                "series_name": None,
                "year": 2019,
                "director": "Félix Dumont-Turgeon",
                "genres": ["Action", "Thriller", "Crime"],
                "rating": 7.1,
                "my_rating": 8,
                "watch_date": "2024-01-15T00:00:00",
                "description": "",
                "poster_url": "https://image.tmdb.org/t/p/w500/fgpKUHugvbHir5Ia51vXKdCZd1F.jpg",
                "content_type": "MOVIE"
            }
        }
