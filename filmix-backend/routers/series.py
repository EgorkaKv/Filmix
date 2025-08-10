from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from models.movie import Movie, MovieCreate, MovieUpdate, ContentType
from services.movie_service import movie_service
from services.tmdb_service import tmdb_service
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

@router.get("/search", response_model=Dict)
async def search_series(query: str = Query(..., description="Поисковый запрос")):
    """Поиск сериалов в TMDB"""
    logger.info(f"Поиск сериалов в TMDB: {query}")
    try:
        # Поиск в TMDB
        search_results = await tmdb_service.search_tv_shows(query)

        # Форматирование результатов
        formatted_results = tmdb_service.format_search_results(search_results, ContentType.SERIES)

        result = {
            "total_results": search_results.get("total_results", 0),
            "total_pages": search_results.get("total_pages", 0),
            "current_page": search_results.get("page", 1),
            "results": formatted_results
        }

        logger.info(f"Найдено {len(formatted_results)} сериалов")
        return result

    except Exception as e:
        logger.error(f"Ошибка при поиске сериалов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске сериалов: {str(e)}")

@router.post("/add-from-tmdb/{tmdb_id}", response_model=Movie)
async def add_series_from_tmdb(tmdb_id: int):
    """Добавить сериал из TMDB по ID"""
    logger.info(f"Добавление сериала из TMDB с ID: {tmdb_id}")
    try:
        # Получаем детали сериала из TMDB
        tmdb_data = await tmdb_service.get_tv_details(tmdb_id)

        # Конвертируем данные TMDB в формат нашей модели
        series_data = tmdb_service.convert_tmdb_to_movie_data(tmdb_data, ContentType.SERIES)

        # Создаем объект MovieCreate
        series_create = MovieCreate(**series_data)

        # Сохраняем в базу данных
        new_series = await movie_service.create_movie(series_create)

        logger.info(f"Сериал успешно добавлен: {new_series.title}")
        return new_series

    except Exception as e:
        logger.error(f"Ошибка при добавлении сериала из TMDB: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении сериала: {str(e)}")
