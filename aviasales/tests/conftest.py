"""Pytest fixtures for Aviasales API tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """TestClient with lifespan loading XML; use context manager for lifespan to run."""
    with TestClient(app) as c:
        yield c
