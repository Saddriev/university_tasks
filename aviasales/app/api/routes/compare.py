"""Comparison endpoint."""

from fastapi import APIRouter

from app.api.deps import ItinerariesDep
from app.schemas import ComparisonResponse
from app.services import compare_itineraries

router = APIRouter()


@router.get(
    "/flights/compare",
    response_model=ComparisonResponse,
    summary="Сравнить результаты двух запросов",
    description="Различия между двумя XML: только в первом, только во втором, изменения цен",
)
def compare(itineraries: ItinerariesDep):
    first, second = itineraries
    return ComparisonResponse(**compare_itineraries(first, second))
