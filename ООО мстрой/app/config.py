"""
Настройки приложения: хост, порт, путь к файлу данных.
Читаются из переменных окружения и .env.
"""
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация сервера и путь к JSON с элементами дерева."""

    host: str = "127.0.0.1"
    port: int = 8000
    data_file: Path = (
        Path(__file__).resolve().parent.parent / "data" / "items.json"
    )

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
