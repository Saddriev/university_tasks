# -*- coding: utf-8 -*-
"""ORM-модель: запись сокращённой ссылки."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db import Base


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class ShortUrl(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    original_url = Column(String(4096), nullable=False, index=True)
    short_code = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=_now_utc)
