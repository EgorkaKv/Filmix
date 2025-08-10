from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.mongodb import connect_to_mongo, close_mongo_connection
from routers import movies, series
from utils.logger import filmix_logger
import logging

# Инициализируем логгирование
logger = logging.getLogger("filmix.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения Filmix API")
    # Подключение к базе данных при запуске
    try:
        await connect_to_mongo()
        logger.info("База данных успешно подключена")
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise

    yield

    # Закрытие подключения при завершении
    logger.info("Завершение работы приложения")
    await close_mongo_connection()

app = FastAPI(
    title="Filmix API",
    description="API для управления коллекцией фильмов и сериалов",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(movies.router)
app.include_router(series.router)

@app.get("/")
async def root():
    logger.info("Запрос к корневому эндпоинту")
    return {"message": "Добро пожаловать в Filmix API"}

@app.get("/health")
async def health_check():
    logger.debug("Проверка здоровья системы")
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Запуск сервера через uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=8000)
