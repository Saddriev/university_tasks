'''
Сервисы бизнес-логики. Экспортируем под старыми именами для совместимости с API.
'''

from app.services.flights import (
    compare_itineraries,
    filter_by_route,
    find_cheapest,
    find_fastest,
    find_most_expensive,
    find_optimal,
    find_slowest,
)

__all__ = [
    "compare_itineraries",
    "filter_by_route",
    "find_cheapest",
    "find_fastest",
    "find_most_expensive",
    "find_optimal",
    "find_slowest",
]
