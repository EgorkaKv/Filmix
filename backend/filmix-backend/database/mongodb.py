from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
import os

# Создаем логгер для этого модуля
logger = logging.getLogger("filmix.database")

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

# Инициализация подключения к MongoDB
async def connect_to_mongo():
    try:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        logger.info(f"Подключение к MongoDB: {mongodb_url}")

        MongoDB.client = AsyncIOMotorClient(mongodb_url)
        MongoDB.database = MongoDB.client.filmix

        # Проверяем подключение
        await MongoDB.client.admin.command('ping')
        logger.info("Успешно подключились к MongoDB")

        # Проверяем количество документов в коллекции movies
        count = await MongoDB.database.movie.count_documents({})
        logger.info(f"Найдено {count} документов в коллекции movie")

    except ConnectionFailure as e:
        logger.error(f"Не удалось подключиться к MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при подключении к MongoDB: {e}")
        raise

async def close_mongo_connection():
    if MongoDB.client is not None:
        MongoDB.client.close()
        logger.info("Подключение к MongoDB закрыто")

def get_database():
    logger.debug("Запрос базы данных...")
    if MongoDB.database is None:
        logger.error("База данных не инициализирована! Вызовите connect_to_mongo() сначала")
        return None

    logger.debug(f"Возвращаем базу данных: {MongoDB.database}")
    return MongoDB.database
