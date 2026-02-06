'''
Доменные модели: рейс, цены и маршрут (итоговый перелёт).
'''

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Flight:
    '''Один сегмент рейса: перевозчик, маршрут, время.'''

    carrier_id: str
    carrier_name: str
    flight_number: str
    source: str
    destination: str
    departure_timestamp: Optional[datetime]
    arrival_timestamp: Optional[datetime]
    class_code: str
    number_of_stops: int
    ticket_type: str

    def asdict(self) -> dict:
        '''Словарь для сериализации в JSON.'''
        return {
            "carrier_id": self.carrier_id,
            "carrier_name": self.carrier_name,
            "flight_number": self.flight_number,
            "source": self.source,
            "destination": self.destination,
            "departure_timestamp": (
                self.departure_timestamp.isoformat() if self.departure_timestamp else None
            ),
            "arrival_timestamp": (
                self.arrival_timestamp.isoformat() if self.arrival_timestamp else None
            ),
            "class_code": self.class_code,
            "number_of_stops": self.number_of_stops,
            "ticket_type": self.ticket_type,
        }


@dataclass
class Pricing:
    '''Цены и сервисные сборы по маршруту.'''

    currency: str
    service_charges: dict

    @property
    def total_adult(self) -> float:
        '''Сумма для одного взрослого (TotalAmount).'''
        return self.service_charges.get("SingleAdult_TotalAmount", 0.0)

    def asdict(self) -> dict:
        '''Словарь для ответа API.'''
        return {
            "currency": self.currency,
            "total_adult": self.total_adult,
            "service_charges": self.service_charges,
        }


@dataclass
class FlightItinerary:
    '''Маршрут: рейсы туда, обратно и цены.'''

    onward_flights: List[Flight]
    return_flights: List[Flight]
    pricing: Optional[Pricing]

    def __post_init__(self) -> None:
        self.return_flights = self.return_flights or []

    @property
    def source(self) -> str:
        '''Аэропорт вылета (из первого сегмента туда).'''
        return self.onward_flights[0].source if self.onward_flights else ""

    @property
    def destination(self) -> str:
        '''Аэропорт прилёта (из последнего сегмента туда).'''
        return self.onward_flights[-1].destination if self.onward_flights else ""

    @property
    def total_duration_minutes(self) -> int:
        '''Общая длительность в минутах (от первого вылета до последнего прилёта туда).'''
        if not self.onward_flights:
            return 0
        first_dep = self.onward_flights[0].departure_timestamp
        last_arr = self.onward_flights[-1].arrival_timestamp
        if first_dep and last_arr:
            return int((last_arr - first_dep).total_seconds() / 60)
        return 0

    @property
    def total_price(self) -> float:
        '''Итоговая цена по прайсингу.'''
        return self.pricing.total_adult if self.pricing else 0.0

    @property
    def currency(self) -> str:
        '''Валюта из прайсинга.'''
        return self.pricing.currency if self.pricing else ""

    def asdict(self) -> dict:
        '''Словарь для ответа API.'''
        return {
            "onward_flights": [f.asdict() for f in self.onward_flights],
            "return_flights": [f.asdict() for f in self.return_flights],
            "source": self.source,
            "destination": self.destination,
            "total_duration_minutes": self.total_duration_minutes,
            "total_price": self.total_price,
            "currency": self.currency,
            "pricing": self.pricing.asdict() if self.pricing else {},
        }
