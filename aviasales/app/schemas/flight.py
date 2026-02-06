"""Pydantic schemas for flight API responses."""

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class FlightResponse(BaseModel):
    """Single flight segment schema."""

    carrier_id: str = Field(..., description="ID авиакомпании")
    carrier_name: str = Field(..., description="Название авиакомпании")
    flight_number: str = Field(..., description="Номер рейса")
    source: str = Field(..., description="Аэропорт отправления (IATA)")
    destination: str = Field(..., description="Аэропорт прибытия (IATA)")
    departure_timestamp: Optional[str] = Field(None, description="Время отправления ISO")
    arrival_timestamp: Optional[str] = Field(None, description="Время прибытия ISO")
    class_code: str = Field(..., description="Класс обслуживания")
    number_of_stops: int = Field(..., description="Количество пересадок")
    ticket_type: str = Field(..., description="Тип билета")


class ItineraryResponse(BaseModel):
    """Itinerary response schema."""

    onward_flights: List[dict] = Field(..., description="Рейсы туда")
    return_flights: List[dict] = Field(..., description="Рейсы обратно")
    source: str = Field(..., description="Аэропорт отправления")
    destination: str = Field(..., description="Аэропорт прибытия")
    total_duration_minutes: int = Field(..., description="Длительность в минутах")
    total_price: float = Field(..., description="Общая цена")
    currency: str = Field(..., description="Валюта")
    pricing: dict = Field(..., description="Детали ценообразования")


class ComparisonResponse(BaseModel):
    """Comparison of two itinerary lists."""

    only_in_first: List[dict] = Field(
        ..., description="Только в первом запросе"
    )
    only_in_second: List[dict] = Field(
        ..., description="Только во втором запросе"
    )
    price_changes: List[dict] = Field(
        ..., description="Изменения цен"
    )
    total_first: int = Field(..., description="Всего в первом")
    total_second: int = Field(..., description="Всего во втором")
