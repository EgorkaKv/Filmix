import logging
import sys
from pathlib import Path

def setup_logging():
    """Настройка логгирования для проекта"""
    # Создаем папку для логов если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Настраиваем форматирование
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Настраиваем логгер для приложения
    logger = logging.getLogger("filmix")
    logger.setLevel(logging.DEBUG)

    # Хэндлер для записи в файл
    file_handler = logging.FileHandler(log_dir / "filmix.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Хэндлер для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем хэндлеры к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Создаем логгер для использования в других модулях
filmix_logger = setup_logging()
