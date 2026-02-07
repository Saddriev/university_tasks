"""
Настройки приложения: хост, порт, URL Hacker News, таймаут запросов.
Читаются из переменных окружения и .env.
"""
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация прокси-сервера и upstream (Hacker News)."""

    host: str = "127.0.0.1"
    port: int = 8232
    hn_base_url: str = "https://news.ycombinator.com"
    request_timeout: float = Field(
        default=30.0,
        gt=0,
        description="Таймаут запроса к Hacker News (секунды).",
    )

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
