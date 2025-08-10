from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from models.movie import Movie, MovieCreate, MovieUpdate, ContentType
from database.mongodb import get_database
import logging

# Создаем логгер для этого модуля
logger = logging.getLogger("filmix.movie_service")


class MovieService:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = None
        logger.info("MovieService инициализирован")

    def get_collection(self) -> AsyncIOMotorCollection:
        if self.collection is None:
            logger.info("Получение коллекции из базы данных...")
            db = get_database()
            logger.info(f"База данных получена: {db}")

            if db is None:
                logger.error("База данных None! Проблема с подключением")
                raise Exception("Не удалось получить базу данных")

            self.collection = db.movie
            logger.info(f"Коллекция movies получена: {self.collection}")

        return self.collection

    async def create_movie(self, movie_data: MovieCreate) -> Movie:
        """Создание нового фильма/сериала"""
        collection = self.get_collection()
        movie_dict = movie_data.model_dump()

        result = await collection.insert_one(movie_dict)
        movie_dict["_id"] = str(result.inserted_id)

        return Movie(**movie_dict)

    async def get_all_movies(self, content_type: Optional[ContentType] = None) -> List[Movie]:
        """Получение всех фильмов или сериалов"""
        logger.info(f"Запрос всех фильмов, content_type: {content_type}")

        collection = self.get_collection()
        logger.info(f"Коллекция получена: {collection}")

        query = {}
        if content_type:
            query["content_type"] = content_type.value

        logger.info(f"Запрос к базе: {query}")

        cursor = collection.find(query).sort("my_rating", -1)
        logger.info(f"Курсор создан: {cursor}")

        movies = []
        count = 0

        async for movie_doc in cursor:
            count += 1
            logger.debug(f"Обработка документа #{count}: {movie_doc.get('title', 'Unknown')}")
            movie_doc["_id"] = str(movie_doc["_id"])
            movies.append(Movie(**movie_doc))

        logger.info(f"Найдено {count} фильмов/сериалов")
        return movies

    async def get_movie_by_id(self, movie_id: str) -> Optional[Movie]:
        """Получение фильма по ID"""
        collection = self.get_collection()

        if not ObjectId.is_valid(movie_id):
            return None

        movie_doc = await collection.find_one({"_id": ObjectId(movie_id)})

        if movie_doc:
            movie_doc["_id"] = str(movie_doc["_id"])
            return Movie(**movie_doc)

        return None

    async def update_movie(self, movie_id: str, movie_update: MovieUpdate) -> Optional[Movie]:
        """Обновление фильма"""
        collection = self.get_collection()

        if not ObjectId.is_valid(movie_id):
            return None

        update_data = {k: v for k, v in movie_update.model_dump().items() if v is not None}

        if not update_data:
            return await self.get_movie_by_id(movie_id)

        result = await collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            return await self.get_movie_by_id(movie_id)

        return None

    async def delete_movie(self, movie_id: str) -> bool:
        """Удаление фильма по ID"""
        logger.info(f"Удаление фильма с ID: {movie_id}")
        collection = self.get_collection()

        if not ObjectId.is_valid(movie_id):
            logger.warning(f"Невалидный ID фильма: {movie_id}")
            return False

        result = await collection.delete_one({"_id": ObjectId(movie_id)})
        
        if result.deleted_count > 0:
            logger.info(f"Фильм с ID {movie_id} успешно удален")
            return True
        else:
            logger.warning(f"Фильм с ID {movie_id} не найден для удаления")
            return False

    async def update_movie_rating(self, movie_id: str, my_rating: int) -> Optional[Movie]:
        """Обновление рейтинга фильма"""
        logger.info(f"Обновление рейтинга фильма {movie_id} на {my_rating}")
        collection = self.get_collection()

        if not ObjectId.is_valid(movie_id):
            logger.warning(f"Невалидный ID фильма: {movie_id}")
            return None

        # Проверяем валидность рейтинга
        if my_rating < 1 or my_rating > 100:
            logger.warning(f"Невалидный рейтинг: {my_rating}")
            return None

        result = await collection.update_one(
            {"_id": ObjectId(movie_id)},
            {"$set": {"my_rating": my_rating}}
        )

        if result.modified_count > 0:
            logger.info(f"Рейтинг фильма {movie_id} успешно обновлен")
            return await self.get_movie_by_id(movie_id)
        else:
            logger.warning(f"Фильм с ID {movie_id} не найден для обновления рейтинга")
            return None


# Создаем экземпляр сервиса
movie_service = MovieService()
