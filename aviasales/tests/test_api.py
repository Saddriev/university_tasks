"""API endpoint tests for Aviasales Flight Search."""

from fastapi import status


def test_health_check(client):
    response = client.get('/api/v1/health')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'status' in data
    assert 'itineraries_1' in data
    assert 'itineraries_2' in data


def test_get_flights_dxb_bkk(client):
    response = client.get('/api/v1/flights/dxb-bkk')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'source' in data[0]
        assert 'destination' in data[0]


def test_get_cheapest_dxb_bkk(client):
    response = client.get('/api/v1/flights/dxb-bkk/cheapest')
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    if response.status_code == status.HTTP_200_OK:
        data = response.json()
        assert 'total_price' in data


def test_compare_flights(client):
    response = client.get('/api/v1/flights/compare')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'only_in_first' in data
    assert 'only_in_second' in data
    assert 'price_changes' in data
