from fastapi import APIRouter, HTTPException
from typing import List
from models.movie import Movie, MovieCreate, MovieUpdate, ContentType
from services.movie_service import movie_service
import logging

# Создаем логгер для этого модуля
logger = logging.getLogger("filmix.movies_router")

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("/", response_model=List[Movie])
async def get_all_movies():
    """Получить все фильмы"""
    logger.info("Запрос всех фильмов")
    try:
        movies = await movie_service.get_all_movies(ContentType.MOVIE)
        logger.info(f"Успешно получено {len(movies)} фильмов")
        return movies
    except Exception as e:
        logger.error(f"Ошибка при получении фильмов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении фильмов: {str(e)}")

@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: str):
    """Получить фильм по ID"""
    logger.info(f"Запрос фильма с ID: {movie_id}")
    try:
        movie = await movie_service.get_movie_by_id(movie_id)
        if movie is None:
            logger.warning(f"Фильм с ID {movie_id} не найден")
            raise HTTPException(status_code=404, detail="Фильм не найден")
        logger.info(f"Фильм найден: {movie.title}")
        return movie
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении фильма {movie_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Movie)
async def create_movie(movie: MovieCreate):
    """Создать новый фильм"""
    logger.info(f"Создание нового фильма: {movie.title}")
    try:
        new_movie = await movie_service.create_movie(movie)
        logger.info(f"Фильм успешно создан с ID: {new_movie.id}")
        return new_movie
    except Exception as e:
        logger.error(f"Ошибка при создании фильма: {e}")
        raise HTTPException(status_code=500, detail=str(e))
