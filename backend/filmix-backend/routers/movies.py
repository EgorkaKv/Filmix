from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from models.movie import Movie, MovieCreate, MovieUpdate, MovieUpdateRating, ContentType
from services.movie_service import movie_service
from services.tmdb_service import tmdb_service
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

@router.get("/search/tmdb", response_model=Dict)
async def search_movies(query: str = Query(..., description="Поисковый запрос")):
    """Поиск фильмов в TMDB"""
    logger.info(f"Поиск фильмов в TMDB: {query}")
    try:
        # Поиск в TMDB
        search_results = await tmdb_service.search_movies(query)

        # Форматирование результатов
        formatted_results = tmdb_service.format_search_results(search_results, ContentType.MOVIE)

        result = {
            "total_results": search_results.get("total_results", 0),
            "total_pages": search_results.get("total_pages", 0),
            "current_page": search_results.get("page", 1),
            "results": formatted_results
        }

        logger.info(f"Найдено {len(formatted_results)} фильмов")
        return result

    except Exception as e:
        logger.error(f"Ошибка при поиске фильмов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске фильмов: {str(e)}")

@router.post("/add-from-tmdb/{tmdb_id}", response_model=Movie)
async def add_movie_from_tmdb(tmdb_id: int):
    """Добавить фильм из TMDB по ID"""
    logger.info(f"Добавление фильма из TMDB с ID: {tmdb_id}")
    try:
        # Проверяем, не существует ли уже фильм с таким TMDB ID
        # (Пока пропускаем эту проверку, можно добавить позже)

        # Получаем детали фильма из TMDB
        tmdb_data = await tmdb_service.get_movie_details(tmdb_id)

        # Конвертируем данные TMDB в формат нашей модели
        movie_data = tmdb_service.convert_tmdb_to_movie_data(tmdb_data, ContentType.MOVIE)

        # Создаем объект MovieCreate
        movie_create = MovieCreate(**movie_data)

        # Сохраняем в базу данных
        new_movie = await movie_service.create_movie(movie_create)

        logger.info(f"Фильм успешно добавлен: {new_movie.title}")
        return new_movie

    except Exception as e:
        logger.error(f"Ошибка при добавлении фильма из TMDB: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении фильма: {str(e)}")

@router.delete("/{movie_id}")
async def delete_movie(movie_id: str):
    """Удалить фильм по ID"""
    logger.info(f"Удаление фильма с ID: {movie_id}")
    try:
        # Проверяем, существует ли фильм
        movie = await movie_service.get_movie_by_id(movie_id)
        if movie is None:
            logger.warning(f"Фильм с ID {movie_id} не найден")
            raise HTTPException(status_code=404, detail="Фильм не найден")

        # Удаляем фильм
        success = await movie_service.delete_movie(movie_id)

        if success:
            logger.info(f"Фильм {movie.title} успешно удален")
            return {"message": f"Фильм '{movie.title}' успешно удален"}
        else:
            logger.error(f"Не удалось удалить фильм с ID {movie_id}")
            raise HTTPException(status_code=500, detail="Не удалось удалить фильм")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при удалении фильма {movie_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении фильма: {str(e)}")

@router.patch("/{movie_id}/rating", response_model=Movie)
async def update_movie_rating(movie_id: str, rating_data: MovieUpdateRating):
    """Обновить рейтинг фильма"""
    logger.info(f"Обновление рейтинга фильма {movie_id} на {rating_data.my_rating}")
    try:
        # Проверяем, существует ли фильм
        existing_movie = await movie_service.get_movie_by_id(movie_id)
        if existing_movie is None:
            logger.warning(f"Фильм с ID {movie_id} не найден")
            raise HTTPException(status_code=404, detail="Фильм не найден")

        # Обновляем рейтинг
        updated_movie = await movie_service.update_movie_rating(movie_id, rating_data.my_rating)

        if updated_movie is None:
            logger.error(f"Не удалось обновить рейтинг фильма с ID {movie_id}")
            raise HTTPException(status_code=500, detail="Не удалось обновить рейтинг фильма")

        logger.info(f"Рейтинг фильма {updated_movie.title} успешно обновлен на {rating_data.my_rating}")
        return updated_movie

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обновлении рейтинга фильма {movie_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении рейтинга: {str(e)}")
