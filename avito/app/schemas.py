# -*- coding: utf-8 -*-
"""Схемы запросов/ответов API."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

URL_MAX = 4096


class CreateRequest(BaseModel):
    """POST /api/v1/shorten — тело запроса."""

    original_url: str = Field(..., max_length=URL_MAX, description="Исходный URL")
    custom_code: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Желаемый короткий код",
    )


class CreateResponse(BaseModel):
    """Ответ после создания короткой ссылки."""

    model_config = ConfigDict(from_attributes=True)

    short_url: str
    original_url: str
    short_code: str
