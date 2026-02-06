'''
Парсинг XML Aviasales: извлечение маршрутов и цен в доменные модели.
'''

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

from app.models import Flight, FlightItinerary, Pricing

TS_FMT = "%Y-%m-%dT%H%M"


class AviasalesXmlParser:
    '''Парсер XML Aviasales.'''

    def __init__(self, path: Union[str, Path]) -> None:
        self._tree = ET.parse(path)
        self._root = self._tree.getroot()

    def _text(self, parent: Optional[ET.Element], tag: str, default: str = "") -> str:
        if parent is None:
            return default
        child = parent.find(tag)
        return (child.text or "").strip() if child is not None else default

    def _ts(self, s: str) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.strptime(s.strip(), TS_FMT)
        except ValueError:
            return None

    def _flight_from_node(self, node: ET.Element) -> Flight:
        carrier = node.find("Carrier")
        cid = carrier.get("id", "") if carrier is not None else ""
        cname = (carrier.text or "").strip() if carrier is not None else ""
        return Flight(
            carrier_id=cid,
            carrier_name=cname,
            flight_number=self._text(node, "FlightNumber"),
            source=self._text(node, "Source"),
            destination=self._text(node, "Destination"),
            departure_timestamp=self._ts(self._text(node, "DepartureTimeStamp")),
            arrival_timestamp=self._ts(self._text(node, "ArrivalTimeStamp")),
            class_code=self._text(node, "Class"),
            number_of_stops=int(self._text(node, "NumberOfStops") or "0"),
            ticket_type=self._text(node, "TicketType"),
        )

    def _flights_from_parent(self, parent: Optional[ET.Element]) -> List[Flight]:
        if parent is None:
            return []
        container = parent.find("Flights")
        if container is None:
            return []
        return [self._flight_from_node(n) for n in container]

    def _pricing_from_node(self, node: Optional[ET.Element]) -> Optional[Pricing]:
        if node is None:
            return None
        currency = node.get("currency", "")
        charges: dict = {}
        for c in node.findall("ServiceCharges"):
            key = f"{c.get('type', '')}_{c.get('ChargeType', '')}"
            try:
                charges[key] = float((c.text or "0").strip())
            except ValueError:
                charges[key] = 0.0
        return Pricing(currency=currency, service_charges=charges)

    def _itinerary_from_block(self, block: ET.Element) -> Optional[FlightItinerary]:
        onward = block.find("OnwardPricedItinerary")
        onward_flights = self._flights_from_parent(onward)
        if not onward_flights:
            return None
        ret = block.find("ReturnPricedItinerary")
        return_flights = self._flights_from_parent(ret)
        pricing = self._pricing_from_node(block.find("Pricing"))
        return FlightItinerary(
            onward_flights=onward_flights,
            return_flights=return_flights,
            pricing=pricing,
        )

    def parse(self) -> List[FlightItinerary]:
        '''Разбирает файл и возвращает список маршрутов.'''
        result: List[FlightItinerary] = []
        for block in self._root.iter("Flights"):
            if block.find("OnwardPricedItinerary") is None:
                continue
            it = self._itinerary_from_block(block)
            if it is not None:
                result.append(it)
        return result


def parse_flights_xml(path: Union[str, Path]) -> List[FlightItinerary]:
    '''
    Читает файл XML и возвращает список маршрутов (FlightItinerary).
    '''
    return AviasalesXmlParser(path).parse()
