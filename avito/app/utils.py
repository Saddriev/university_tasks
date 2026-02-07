# -*- coding: utf-8 -*-
"""Валидация URL/кода, генерация случайного кода."""

import re
import secrets
import string
from urllib.parse import urlparse

import httpx

_CODE_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,50}$")


def make_code(length: int = 6) -> str:
    """Случайный URL-safe код (буквы + цифры)."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def is_valid_slug(slug: str) -> bool:
    """Проверка формата кастомного кода."""
    return bool(slug and _CODE_PATTERN.fullmatch(slug))


def check_url_reachable(url: str, timeout: float = 5.0) -> bool:
    """
    URL должен быть http(s) и отдавать 2xx/3xx.
    Пробуем HEAD, затем GET.
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        if parsed.scheme not in ("http", "https"):
            return False
    except Exception:
        return False

    for method in ("head", "get"):
        try:
            if method == "head":
                r = httpx.head(url, timeout=timeout, follow_redirects=True)
            else:
                r = httpx.get(url, timeout=timeout, follow_redirects=True)
            if r.status_code < 400:
                return True
        except (httpx.HTTPError, OSError):
            pass
    return False
