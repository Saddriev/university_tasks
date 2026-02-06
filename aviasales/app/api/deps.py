"""FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends, Request


def get_itineraries(request: Request) -> tuple[list, list]:
    """Return loaded itineraries from app state."""
    return request.app.state.itineraries_1, request.app.state.itineraries_2


ItinerariesDep = Annotated[tuple[list, list], Depends(get_itineraries)]
