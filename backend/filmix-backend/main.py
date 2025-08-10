from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.mongodb import connect_to_mongo, close_mongo_connection
from routers import movies, series
from fastapi.middleware.cors import CORSMiddleware
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

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(movies.router)
app.include_router(series.router)

@app.get("/")
async def root():
    return {
        "message": "Filmix Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
