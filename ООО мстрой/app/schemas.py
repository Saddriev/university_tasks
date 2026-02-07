"""Схемы запросов и ответов для эндпоинтов дерева."""
from typing import Any, Union

from pydantic import BaseModel


class ItemIdRequest(BaseModel):
    """Запрос с id элемента."""

    id: Any


class TreeStoreRequest(BaseModel):
    """Запрос с массивом элементов для инициализации дерева."""

    items: list[dict[str, Any]]


class TreeStoreResponse(BaseModel):
    """Ответ API: результат операции (массив, объект или None)."""

    result: Union[list[dict[str, Any]], dict[str, Any], None]
