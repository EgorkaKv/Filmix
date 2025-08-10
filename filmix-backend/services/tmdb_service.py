import httpx
import os
from typing import List, Dict
import logging
from models.movie import ContentType

logger = logging.getLogger("filmix.tmdb_service")

class TMDBService:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = os.getenv("TMDB_BASE_URL")
        self.image_base_url = os.getenv("TMDB_IMAGE_BASE_URL")

        if not self.api_key:
            print('TMDB_API_KEY:', self.api_key)
            raise ValueError("TMDB_API_KEY не найден в переменных окружения")

        logger.info("TMDB сервис инициализирован")

    async def search_movies(self, query: str, page: int = 1) -> Dict:
        """Поиск фильмов в TMDB"""
        logger.info(f"Поиск фильмов по запросу: {query}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/search/movie",
                    params={
                        "api_key": self.api_key,
                        "query": query,
                        "page": page,
                        "language": "ru-RU"
                    }
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Найдено {data.get('total_results', 0)} результатов")
                return data

            except httpx.HTTPError as e:
                logger.error(f"Ошибка при поиске фильмов: {e}")
                raise
            except Exception as e:
                logger.error(f"Неожиданная ошибка при поиске: {e}")
                raise

    async def search_tv_shows(self, query: str, page: int = 1) -> Dict:
        """Поиск сериалов в TMDB"""
        logger.info(f"Поиск сериалов по запросу: {query}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/search/tv",
                    params={
                        "api_key": self.api_key,
                        "query": query,
                        "page": page,
                        "language": "ru-RU"
                    }
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Найдено {data.get('total_results', 0)} результатов")
                return data

            except httpx.HTTPError as e:
                logger.error(f"Ошибка при поиске сериалов: {e}")
                raise
            except Exception as e:
                logger.error(f"Неожиданная ошибка при поиске: {e}")
                raise

    async def get_movie_details(self, movie_id: int) -> Dict:
        """Получить детальную информацию о фильме"""
        logger.info(f"Получение деталей фильма с TMDB ID: {movie_id}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/movie/{movie_id}",
                    params={
                        "api_key": self.api_key,
                        "language": "ru-RU"
                    }
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Получены детали фильма: {data.get('title', 'Неизвестно')}")
                return data

            except httpx.HTTPError as e:
                logger.error(f"Ошибка при получении деталей фильма: {e}")
                raise
            except Exception as e:
                logger.error(f"Неожиданная ошибка при получении деталей: {e}")
                raise

    async def get_tv_details(self, tv_id: int) -> Dict:
        """Получить детальную информацию о сериале"""
        logger.info(f"Получение деталей сериала с TMDB ID: {tv_id}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/tv/{tv_id}",
                    params={
                        "api_key": self.api_key,
                        "language": "ru-RU"
                    }
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Получены детали сериала: {data.get('name', 'Неизвестно')}")
                return data

            except httpx.HTTPError as e:
                logger.error(f"Ошибка при получении деталей сериала: {e}")
                raise
            except Exception as e:
                logger.error(f"Неожиданная ошибка при получении деталей: {e}")
                raise

    def format_search_results(self, results: Dict, content_type: ContentType) -> List[Dict]:
        """Форматирование результатов поиска для фронтенда"""
        formatted_results = []

        for item in results.get('results', []):
            if content_type == ContentType.MOVIE:
                formatted_item = {
                    "tmdb_id": item.get("id"),
                    "title": item.get("title", ""),
                    "original_title": item.get("original_title", ""),
                    "release_date": item.get("release_date", ""),
                    "poster_path": f"{self.image_base_url}{item.get('poster_path')}" if item.get('poster_path') else None,
                    "overview": item.get("overview", ""),
                    "vote_average": item.get("vote_average", 0),
                    "content_type": content_type.value
                }
            else:  # TV Show
                formatted_item = {
                    "tmdb_id": item.get("id"),
                    "title": item.get("name", ""),
                    "original_title": item.get("original_name", ""),
                    "release_date": item.get("first_air_date", ""),
                    "poster_path": f"{self.image_base_url}{item.get('poster_path')}" if item.get('poster_path') else None,
                    "overview": item.get("overview", ""),
                    "vote_average": item.get("vote_average", 0),
                    "content_type": content_type.value
                }

            formatted_results.append(formatted_item)

        return formatted_results

    def convert_tmdb_to_movie_data(self, tmdb_data: Dict, content_type: ContentType) -> Dict:
        """Конвертация данных TMDB в формат нашей модели Movie"""
        if content_type == ContentType.MOVIE:
            return {
                "title": tmdb_data.get("title", ""),
                "original_title": tmdb_data.get("original_title", ""),
                "original_language": tmdb_data.get("original_language", ""),
                "year": int(tmdb_data.get("release_date", "1900-01-01")[:4]) if tmdb_data.get("release_date") else None,
                "director": self._extract_director(tmdb_data),
                "genres": [genre["name"] for genre in tmdb_data.get("genres", [])],
                "rating": round(tmdb_data.get("vote_average", 0), 1),
                "description": tmdb_data.get("overview", ""),
                "poster_url": f"{self.image_base_url}{tmdb_data.get('poster_path')}" if tmdb_data.get('poster_path') else None,
                "content_type": content_type.value,
                "watch_date": None,
                "my_rating": None,
                "series_name": None
            }
        else:  # TV Show
            return {
                "title": tmdb_data.get("name", ""),
                "original_title": tmdb_data.get("original_name", ""),
                "original_language": tmdb_data.get("original_language", ""),
                "year": int(tmdb_data.get("first_air_date", "1900-01-01")[:4]) if tmdb_data.get("first_air_date") else None,
                "director": self._extract_creator(tmdb_data),
                "genres": [genre["name"] for genre in tmdb_data.get("genres", [])],
                "rating": round(tmdb_data.get("vote_average", 0), 1),
                "description": tmdb_data.get("overview", ""),
                "poster_url": f"{self.image_base_url}{tmdb_data.get('poster_path')}" if tmdb_data.get('poster_path') else None,
                "content_type": content_type.value,
                "watch_date": None,
                "my_rating": None,
                "series_name": None
            }

    def _extract_director(self, tmdb_data: Dict) -> str:
        """Извлечение режиссера из данных фильма (требует дополнительный запрос для получения crew)"""
        # Пока возвращаем пустую строку, позже можно добавить запрос на получение crew
        return ""

    def _extract_creator(self, tmdb_data: Dict) -> str:
        """Извлечение создателя из данных сериала"""
        creators = tmdb_data.get("created_by", [])
        if creators:
            return creators[0].get("name", "")
        return ""

# Создаем единственный экземпляр сервиса
tmdb_service = TMDBService()
