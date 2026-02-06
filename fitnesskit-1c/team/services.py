"""
Клиент к 1С: запрос GetSpecialistList и маппинг в формат API.
"""
import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

REQUIRED_EMPLOYEE_KEYS = ("id", "name", "last_name", "phone", "image_url")


def _safe_str(value) -> str:
    """Приводит значение к строке; при отсутствии — пустая строка."""
    if value is None:
        return ""
    return str(value).strip()


def _get_first_key(obj: dict, *keys: str):
    """Возвращает значение первого существующего ключа или None."""
    if not isinstance(obj, dict):
        return None
    for k in keys:
        if obj.get(k) is not None:
            return obj[k]
    return None


def _map_specialist_to_employee(raw) -> dict:
    """
    Преобразует элемент ответа 1С в формат id, name, last_name, phone, image_url.
    Учитываются разные варианты имён полей в 1С. Не-словарь → пустые строки.
    """
    if not isinstance(raw, dict):
        return {k: "" for k in REQUIRED_EMPLOYEE_KEYS}

    return {
        "id": _safe_str(_get_first_key(
            raw, "id", "Id", "GUID", "guid", "SpecialistId")),
        "name": _safe_str(_get_first_key(
            raw, "name", "Name", "FirstName", "Имя")),
        "last_name": _safe_str(_get_first_key(
            raw, "last_name", "LastName", "Surname", "Фамилия")),
        "phone": _safe_str(_get_first_key(
            raw, "phone", "Phone", "PhoneNumber", "Телефон", "Mobile")),
        "image_url": _safe_str(_get_first_key(
            raw, "image_url", "ImageUrl", "Photo", "Image", "Avatar", "Фото")),
    }


def _parse_1c_response(data) -> list:
    """Из ответа 1С извлекает список специалистов. Безопасно к неожиданной структуре."""
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []
    items = (
        data.get("Data")
        or data.get("Result")
        or data.get("Specialists")
        or data.get("SpecialistList")
        or data.get("Items")
        or data.get("employees")
    )
    if items is None and "data" in data:
        inner = data["data"]
        if isinstance(inner, list):
            items = inner
        elif isinstance(inner, dict):
            items = inner.get("Items")
    return items if isinstance(items, list) else []


def fetch_employees_from_1c() -> list:
    """
    POST-запрос к 1С GetSpecialistList.
    Возвращает список сотрудников в формате API.
    При ошибке сети/HTTP логирует и пробрасывает исключение.
    """
    url = settings.ONEC_BASE_URL
    auth = (settings.ONEC_LOGIN, settings.ONEC_PASSWORD)
    body = {
        "Request_id": settings.ONEC_GET_SPECIALIST_REQUEST_ID,
        "ClubId": settings.ONEC_CLUB_ID,
        "Method": "GetSpecialistList",
        "Parameters": {"ServiceId": ""},
    }
    timeout = getattr(settings, "ONEC_TIMEOUT", 5.0)

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=body, auth=auth)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        logger.error(
            "1C HTTP error: status=%s body=%s",
            e.response.status_code,
            (e.response.text or "")[:300],
        )
        raise
    except (httpx.TimeoutException, httpx.ConnectError) as e:
        logger.error("1C request failed: %s", type(e).__name__)
        raise
    except Exception as e:
        logger.exception("1C unexpected error: %s", e)
        raise

    items = _parse_1c_response(data)
    if not items and data:
        logger.warning("1C response has no items: keys=%s", list(data.keys()))
    return [
        _map_specialist_to_employee(item)
        for item in items
        if item is not None
    ]
