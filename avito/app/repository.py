# -*- coding: utf-8 -*-
"""Репозиторий: работа с таблицей short_urls."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import config
from app.models import ShortUrl
from app.utils import make_code

ATTEMPTS = 100


class ShortUrlRepository:
    """Доступ к short_urls."""

    def __init__(self, sess: Session):
        self._sess = sess

    def add(self, long_url: str, slug: Optional[str] = None) -> ShortUrl:
        """Добавить запись. slug — опциональный кастомный код."""
        code = slug if slug else self._unique_code()
        row = ShortUrl(original_url=long_url, short_code=code)
        self._sess.add(row)
        self._sess.commit()
        self._sess.refresh(row)
        return row

    def _unique_code(self) -> str:
        for _ in range(ATTEMPTS):
            c = make_code(length=config.code_len)
            if self.find_by_code(c) is None:
                return c
        raise RuntimeError("Не удалось подобрать уникальный код")

    def find_by_code(self, code: str) -> Optional[ShortUrl]:
        """Найти по short_code."""
        stmt = select(ShortUrl).where(ShortUrl.short_code == code)
        return self._sess.execute(stmt).scalar_one_or_none()
