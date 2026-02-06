"""
API: GET /team/get_employees — список сотрудников из 1С.
При недоступности 1С возвращается тестовый JSON.
"""
import logging

import httpx
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from team.services import fetch_employees_from_1c

logger = logging.getLogger(__name__)

# Тестовые данные при недоступности 1С
TEST_EMPLOYEES = [
    {"id": "1", "name": "Иван", "last_name": "Петров",
     "phone": "+7 999 111-22-33", "image_url": ""},
    {"id": "2", "name": "Мария", "last_name": "Сидорова",
     "phone": "+7 999 444-55-66", "image_url": ""},
    {"id": "3", "name": "Алексей", "last_name": "Козлов",
     "phone": "", "image_url": ""},
]


def _fallback_response():
    """Ответ с тестовыми данными при ошибке интеграции."""
    logger.warning("1C unavailable, returning test data")
    return JsonResponse({"employees": TEST_EMPLOYEES, "test_data": True})


@require_GET
def get_employees(request):
    """
    GET /team/get_employees.
    Получает данные из 1С; при ошибке связи — тестовый JSON.
    """
    try:
        employees = fetch_employees_from_1c()
        return JsonResponse({"employees": employees})
    except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError):
        return _fallback_response()
    except Exception as e:
        msg = str(e).lower()
        if "timed out" in msg or "timeout" in msg:
            return _fallback_response()
        logger.exception("Integration error: %s", e)
        detail = str(e) if settings.DEBUG else "Service temporarily unavailable"
        return JsonResponse(
            {"error": "Integration error", "detail": detail},
            status=502,
        )
