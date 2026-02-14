# -*- coding: utf-8 -*-
"""FastAPI: URL Shortener — shorten + redirect."""

import os
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import config
from app.db import Base, get_db, get_engine
from app.repository import ShortUrlRepository
from app.schemas import CreateRequest, CreateResponse
from app.utils import check_url_reachable, is_valid_slug


def _run_migrations():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini = os.path.join(root, "migrations", "alembic.ini")
    alembic_cfg = Config(ini)
    alembic_cfg.set_main_option("sqlalchemy.url", config.database_url)
    try:
        command.upgrade(alembic_cfg, "head")
    except (CommandError, FileNotFoundError) as exc:
        log.warning("Alembic failed %s, using create_all", exc)
        Base.metadata.create_all(bind=get_engine())


@asynccontextmanager
async def _lifespan(app: FastAPI):
    _run_migrations()
    yield


application = FastAPI(
    title="URL Shortener",
    version="1.0.0",
    lifespan=_lifespan,
)

api_app = FastAPI(title="URL Shortener API", version="1.0.0")


@api_app.post(
    "/shorten",
    response_model=CreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Некорректный URL или код"},
        status.HTTP_409_CONFLICT: {"description": "Код уже занят"},
    },
)
def shorten(payload: CreateRequest, db: Session = Depends(get_db)):
    """Создать короткую ссылку."""
    if not check_url_reachable(payload.original_url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL недоступен или невалиден",
        )

    if payload.custom_code:
        if not is_valid_slug(payload.custom_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Код: 3–50 символов, буквы/цифры/-/_",
            )
        repo = ShortUrlRepository(db)
        if repo.find_by_code(payload.custom_code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Код уже занят",
            )

    repo = ShortUrlRepository(db)
    try:
        row = repo.add(payload.original_url, payload.custom_code)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Код занят (конфликт)",
        ) from None

    base = config.base_url.rstrip("/")
    return CreateResponse(
        short_url=f"{base}/{row.short_code}",
        original_url=row.original_url,
        short_code=row.short_code,
    )


@api_app.get("/health")
def health():
    return {"status": "ok"}


application.mount("/api/v1", api_app)


@application.get(
    "/{short_code}",
    responses={
        status.HTTP_302_FOUND: {"description": "Redirect"},
        status.HTTP_404_NOT_FOUND: {"description": "Не найдено"},
    },
)
def follow(short_code: str, db: Session = Depends(get_db)):
    """Редирект по короткому коду."""
    repo = ShortUrlRepository(db)
    row = repo.find_by_code(short_code)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена",
        )
    return RedirectResponse(
        url=row.original_url,
        status_code=status.HTTP_302_FOUND,
    )


app = application
