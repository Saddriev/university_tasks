'''
Бизнес-логика: фильтрация маршрутов, выбор по цене/времени, сравнение двух списков.
'''

from enum import Enum
from typing import List, Optional

from app.models import FlightItinerary


class Criterion(str, Enum):
    '''Критерий выбора маршрута из списка.'''
    CHEAPEST = "cheapest"
    MOST_EXPENSIVE = "most_expensive"
    FASTEST = "fastest"
    SLOWEST = "slowest"
    OPTIMAL = "optimal"


def filter_by_route(
    itineraries: List[FlightItinerary],
    source: str,
    destination: str,
) -> List[FlightItinerary]:
    '''Оставляет только маршруты откуда -> куда.'''
    return list(filter(
        lambda it: it.source == source and it.destination == destination,
        itineraries,
    ))


def _price_key(it: FlightItinerary) -> float:
    return it.total_price


def _duration_key(it: FlightItinerary) -> float:
    return it.total_duration_minutes


def _optimal_key(it: FlightItinerary) -> float:
    '''Чем меньше — тем лучше.'''
    if it.total_price <= 0 or it.total_duration_minutes <= 0:
        return float("inf")
    return (it.total_price / 100.0) + (it.total_duration_minutes / 10.0)


_CRITERIA = {
    Criterion.CHEAPEST: (_price_key, True),
    Criterion.MOST_EXPENSIVE: (_price_key, False),
    Criterion.FASTEST: (_duration_key, True),
    Criterion.SLOWEST: (_duration_key, False),
    Criterion.OPTIMAL: (_optimal_key, True),
}


def select_by_criterion(
    itineraries: List[FlightItinerary],
    criterion: Criterion,
) -> Optional[FlightItinerary]:
    '''
    Выбирает один маршрут по заданному критерию.
    Пустой список -> None.
    '''
    if not itineraries:
        return None
    key_fn, ascending = _CRITERIA[criterion]
    sorted_list = sorted(itineraries, key=key_fn, reverse=not ascending)
    return sorted_list[0]


def find_cheapest(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    return select_by_criterion(itineraries, Criterion.CHEAPEST)


def find_most_expensive(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    return select_by_criterion(itineraries, Criterion.MOST_EXPENSIVE)


def find_fastest(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    return select_by_criterion(itineraries, Criterion.FASTEST)


def find_slowest(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    return select_by_criterion(itineraries, Criterion.SLOWEST)


def find_optimal(itineraries: List[FlightItinerary]) -> Optional[FlightItinerary]:
    return select_by_criterion(itineraries, Criterion.OPTIMAL)


def _make_key(it: FlightItinerary) -> str:
    segs = "_".join(f"{f.source}-{f.destination}" for f in it.onward_flights)
    return f"{it.source}-{it.destination}_{segs}_{it.total_price}"


def compare_itineraries(
    first: List[FlightItinerary],
    second: List[FlightItinerary],
) -> dict:
    '''
    Сравнивает два набора маршрутов через множество ключей.
    '''
    map1 = {_make_key(it): it for it in first}
    map2 = {_make_key(it): it for it in second}
    keys1 = set(map1)
    keys2 = set(map2)

    only_in_first = [map1[k].asdict() for k in (keys1 - keys2)]
    only_in_second = [map2[k].asdict() for k in (keys2 - keys1)]

    common_keys = keys1 & keys2
    price_changes = []
    for k in common_keys:
        it1, it2 = map1[k], map2[k]
        if it1.total_price != it2.total_price:
            price_changes.append({
                "itinerary": it1.asdict(),
                "price_changed": {"old": it1.total_price, "new": it2.total_price},
            })

    return {
        "only_in_first": only_in_first,
        "only_in_second": only_in_second,
        "price_changes": price_changes,
        "total_first": len(first),
        "total_second": len(second),
    }
