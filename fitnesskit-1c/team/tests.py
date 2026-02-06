"""
Тесты API и сервисов интеграции с 1С.
"""
import json
from unittest.mock import patch

import httpx
from django.test import Client, TestCase

from team.services import (
    REQUIRED_EMPLOYEE_KEYS,
    _map_specialist_to_employee,
    _parse_1c_response,
    fetch_employees_from_1c,
)
from team.views import TEST_EMPLOYEES


class Parse1CResponseTests(TestCase):
    """Тесты разбора ответа 1С."""

    def test_empty_dict_returns_empty_list(self):
        self.assertEqual(_parse_1c_response({}), [])

    def test_non_dict_non_list_returns_empty_list(self):
        self.assertEqual(_parse_1c_response(None), [])
        self.assertEqual(_parse_1c_response("x"), [])

    def test_list_passed_through(self):
        data = [{"id": "1", "Name": "Test"}]
        self.assertEqual(_parse_1c_response(data), data)

    def test_data_key_list(self):
        data = {"Data": [{"id": "1"}]}
        self.assertEqual(_parse_1c_response(data), [{"id": "1"}])

    def test_result_key_list(self):
        data = {"Result": [{"id": "2"}]}
        self.assertEqual(_parse_1c_response(data), [{"id": "2"}])

    def test_inner_data_items(self):
        data = {"data": {"Items": [{"id": "3"}]}}
        self.assertEqual(_parse_1c_response(data), [{"id": "3"}])


class MapSpecialistToEmployeeTests(TestCase):
    """Тесты маппинга специалиста 1С в формат API."""

    def test_required_keys_present(self):
        result = _map_specialist_to_employee({"id": "1", "Name": "Иван"})
        for key in REQUIRED_EMPLOYEE_KEYS:
            self.assertIn(key, result)
        self.assertEqual(result["id"], "1")
        self.assertEqual(result["name"], "Иван")

    def test_non_dict_returns_empty_strings(self):
        result = _map_specialist_to_employee(None)
        self.assertEqual(result, {k: "" for k in REQUIRED_EMPLOYEE_KEYS})

    def test_alternative_field_names(self):
        raw = {"Id": "x", "LastName": "Петров", "Phone": "+7"}
        result = _map_specialist_to_employee(raw)
        self.assertEqual(result["id"], "x")
        self.assertEqual(result["last_name"], "Петров")
        self.assertEqual(result["phone"], "+7")


class GetEmployeesViewTests(TestCase):
    """Тесты эндпоинта GET /team/get_employees."""

    def setUp(self):
        self.client = Client()

    def test_success_returns_employees(self):
        with patch("team.views.fetch_employees_from_1c") as mock_fetch:
            mock_fetch.return_value = [
                {"id": "1", "name": "А", "last_name": "Б",
                 "phone": "", "image_url": ""},
            ]
            resp = self.client.get("/team/get_employees/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn("employees", data)
        self.assertEqual(len(data["employees"]), 1)
        self.assertFalse(data.get("test_data", False))

    def test_fallback_on_timeout_returns_test_data(self):
        with patch("team.views.fetch_employees_from_1c") as mock_fetch:
            mock_fetch.side_effect = httpx.TimeoutException("timeout")
            resp = self.client.get("/team/get_employees/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data.get("test_data"))
        self.assertEqual(len(data["employees"]), len(TEST_EMPLOYEES))

    def test_fallback_on_connect_error(self):
        with patch("team.views.fetch_employees_from_1c") as mock_fetch:
            mock_fetch.side_effect = httpx.ConnectError("connection failed")
            resp = self.client.get("/team/get_employees/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data.get("test_data"))

    def test_502_on_unexpected_error(self):
        with patch("team.views.fetch_employees_from_1c") as mock_fetch:
            mock_fetch.side_effect = ValueError("internal")
            resp = self.client.get("/team/get_employees/")
        self.assertEqual(resp.status_code, 502)
        data = json.loads(resp.content)
        self.assertIn("error", data)


class FetchEmployeesFrom1CTests(TestCase):
    """Тесты запроса к 1С (с моком httpx)."""

    @patch("team.services.httpx.Client")
    def test_returns_mapped_employees(self, mock_client_class):
        enter = mock_client_class.return_value.__enter__.return_value
        mock_response = enter.post.return_value
        mock_response.raise_for_status = lambda: None
        mock_response.json.return_value = {
            "Data": [
                {"Id": "guid-1", "Name": "Иван", "LastName": "Петров"},
            ],
        }
        result = fetch_employees_from_1c()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "guid-1")
        self.assertEqual(result[0]["name"], "Иван")
        self.assertEqual(result[0]["last_name"], "Петров")

    @patch("team.services.httpx.Client")
    def test_raises_on_http_error(self, mock_client_class):
        post = mock_client_class.return_value.__enter__.return_value.post
        post.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "500", request=None, response=post.return_value,
        )
        post.return_value.status_code = 500
        post.return_value.text = "Server Error"
        with self.assertRaises(httpx.HTTPStatusError):
            fetch_employees_from_1c()
