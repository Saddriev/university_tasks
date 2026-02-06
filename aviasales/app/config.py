'''
Конфигурация приложения: читается из окружения и .env.
'''

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''Параметры хоста, порта и путей к XML.'''
    host: str = "127.0.0.1"
    port: int = 8000
    xml_file_1: str = "RS_Via-3.xml"
    xml_file_2: str = "RS_ViaOW.xml"

    model_config = {"env_file": ".env", "case_sensitive": False}


@lru_cache
def get_settings() -> Settings:
    '''Возвращает единственный экземпляр настроек (кэш).'''
    return Settings()
