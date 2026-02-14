# -*- coding: utf-8 -*-
"""Сессии БД: engine, фабрика, dependency."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import config

_connect_args = (
    {"check_same_thread": False}
    if "sqlite" in config.database_url
    else {}
)

_engine = create_engine(config.database_url, connect_args=_connect_args)
_SessionFactory = sessionmaker(
    bind=_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

Base = declarative_base()


def get_db():
    """Depends: сессия с авто-закрытием."""
    sess = _SessionFactory()
    try:
        yield sess
    finally:
        sess.close()


def get_engine():
    """Engine для миграций."""
    return _engine
