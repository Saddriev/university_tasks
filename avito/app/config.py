# -*- coding: utf-8 -*-
"""Конфигурация: env-переменные, валидация."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Параметры приложения из окружения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str = "sqlite:///./urlshortener.db"
    base_url: str = "http://localhost:8000"
    code_len: int = 6

    @field_validator("code_len")
    @classmethod
    def code_len_range(cls, v):
        if not 4 <= v <= 20:
            raise ValueError("code_len 4..20")
        return v


config = AppConfig()
