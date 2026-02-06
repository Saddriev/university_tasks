"""Health check endpoint."""

from fastapi import APIRouter

from app.api.deps import ItinerariesDep

router = APIRouter()


@router.get(
    "/health",
    summary="Проверка состояния сервиса",
    description="Статус работы и количество загруженных перелётов",
)
def health(itineraries: ItinerariesDep):
    first, second = itineraries
    return {
        "status": "ok",
        "itineraries_1": len(first),
        "itineraries_2": len(second),
    }
