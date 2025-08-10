from fastapi import APIRouter, HTTPException
from typing import List
from models.movie import Movie, MovieCreate, MovieUpdate, ContentType
from services.movie_service import movie_service
import logging

# Создаем логгер для этого модуля
logger = logging.getLogger("filmix.series_router")

router = APIRouter(prefix="/api/series", tags=["series"])

@router.get("/", response_model=List[Movie])
async def get_all_series():
    """Получить все сериалы"""
    logger.info("Запрос всех сериалов")
    try:
        series = await movie_service.get_all_movies(ContentType.SERIES)
        logger.info(f"Успешно получено {len(series)} сериалов")
        return series
    except Exception as e:
        logger.error(f"Ошибка при получении сериалов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении сериалов: {str(e)}")

@router.get("/{series_id}", response_model=Movie)
async def get_series(series_id: str):
    """Получить сериал по ID"""
    logger.info(f"Запрос сериала с ID: {series_id}")
    try:
        series = await movie_service.get_movie_by_id(series_id)
        if series is None:
            logger.warning(f"Сериал с ID {series_id} не найден")
            raise HTTPException(status_code=404, detail="Сериал не найден")
        logger.info(f"Сериал найден: {series.title}")
        return series
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении сериала {series_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Movie)
async def create_series(series: MovieCreate):
    """Создать новый сериал"""
    logger.info(f"Создание нового сериала: {series.title}")
    try:
        new_series = await movie_service.create_movie(series)
        logger.info(f"Сериал успешно создан с ID: {new_series.id}")
        return new_series
    except Exception as e:
        logger.error(f"Ошибка при создании сериала: {e}")
        raise HTTPException(status_code=500, detail=str(e))
