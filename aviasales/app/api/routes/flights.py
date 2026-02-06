'''
Эндпоинты поиска перелётов DXB-BKK.
'''

from fastapi import APIRouter, HTTPException, status

from app.api.deps import ItinerariesDep
from app.models import FlightItinerary
from app.schemas import ItineraryResponse
from app.services import (
    filter_by_route,
    find_cheapest,
    find_fastest,
    find_most_expensive,
    find_optimal,
    find_slowest,
)

router = APIRouter()

SOURCE, DEST = "DXB", "BKK"


def _filtered(itineraries: ItinerariesDep) -> list:
    _, second = itineraries
    return filter_by_route(second, SOURCE, DEST)


def _one_or_404(filtered: list, find_fn) -> FlightItinerary:
    '''Вызывает find_fn(filtered) и возвращает результат или 404.'''
    it = find_fn(filtered)
    if it is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No flights found")
    return it


@router.get(
    "/dxb-bkk",
    response_model=list[ItineraryResponse],
    summary="Все варианты перелёта DXB-BKK",
    description="Список всех вариантов перелёта из Дубая (DXB) в Бангкок (BKK)",
)
def get_all(itineraries: ItinerariesDep):
    items = _filtered(itineraries)
    return [ItineraryResponse(**it.asdict()) for it in items]


@router.get(
    "/dxb-bkk/cheapest",
    response_model=ItineraryResponse,
    summary="Самый дешёвый перелёт DXB-BKK",
    responses={404: {"description": "Перелёты не найдены"}},
)
def get_cheapest(itineraries: ItinerariesDep):
    it = _one_or_404(_filtered(itineraries), find_cheapest)
    return ItineraryResponse(**it.asdict())


@router.get(
    "/dxb-bkk/most-expensive",
    response_model=ItineraryResponse,
    summary="Самый дорогой перелёт DXB-BKK",
    responses={404: {"description": "Перелёты не найдены"}},
)
def get_most_expensive(itineraries: ItinerariesDep):
    it = _one_or_404(_filtered(itineraries), find_most_expensive)
    return ItineraryResponse(**it.asdict())


@router.get(
    "/dxb-bkk/fastest",
    response_model=ItineraryResponse,
    summary="Самый быстрый перелёт DXB-BKK",
    responses={404: {"description": "Перелёты не найдены"}},
)
def get_fastest(itineraries: ItinerariesDep):
    it = _one_or_404(_filtered(itineraries), find_fastest)
    return ItineraryResponse(**it.asdict())


@router.get(
    "/dxb-bkk/slowest",
    response_model=ItineraryResponse,
    summary="Самый долгий перелёт DXB-BKK",
    responses={404: {"description": "Перелёты не найдены"}},
)
def get_slowest(itineraries: ItinerariesDep):
    it = _one_or_404(_filtered(itineraries), find_slowest)
    return ItineraryResponse(**it.asdict())


@router.get(
    "/dxb-bkk/optimal",
    response_model=ItineraryResponse,
    summary="Оптимальный перелёт DXB-BKK",
    description="Баланс между ценой и временем в пути",
    responses={404: {"description": "Перелёты не найдены"}},
)
def get_optimal(itineraries: ItinerariesDep):
    it = _one_or_404(_filtered(itineraries), find_optimal)
    return ItineraryResponse(**it.asdict())
