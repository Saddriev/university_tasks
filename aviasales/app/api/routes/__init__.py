"""API route modules."""

from fastapi import APIRouter

from app.api.routes import compare, flights, health

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(flights.router, prefix="/flights", tags=["Flights"])
api_router.include_router(compare.router, tags=["Comparison"])
api_router.include_router(health.router, tags=["Health"])
