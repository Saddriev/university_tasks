'''
Точка входа FastAPI: создание приложения и загрузка данных при старте.
'''

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api.routes import api_router
from app.config import get_settings
from app.parsers import parse_flights_xml

BASE_DIR = Path(__file__).resolve().parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    При старте приложения загружаем оба XML в app.state.
    '''
    settings = get_settings()
    file1 = BASE_DIR / settings.xml_file_1
    file2 = BASE_DIR / settings.xml_file_2

    for path, name in [(file1, "xml_file_1"), (file2, "xml_file_2")]:
        if not path.exists():
            raise FileNotFoundError(f"XML не найден: {name}={path}")

    app.state.itineraries_1 = parse_flights_xml(file1)
    app.state.itineraries_2 = parse_flights_xml(file2)
    yield


app = FastAPI(
    title="Aviasales Flight Search API",
    version="1.0.0",
    description=(
        "Веб-сервис для анализа данных о перелётах из XML файлов партнёров Aviasales. "
        "API для поиска вариантов перелёта, сравнения цен и анализа маршрутов."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router)
