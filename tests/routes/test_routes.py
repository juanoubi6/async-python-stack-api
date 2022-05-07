import json
import unittest
from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient

from app import api
from tests.mock_data.mocks import MOCK_USER

client = TestClient(api)


class TestRoutes(unittest.TestCase):

    @patch.object(api, "user_service")
    def test_get_user_returns_user_on_success(self, mock_user_service):
        mock_user_service.get_user = AsyncMock(return_value=MOCK_USER)

        response = client.get("/users/1")

        assert response.status_code == 200
        assert response.json() == json.loads(MOCK_USER.json())

        mock_user_service.get_user.assert_called_once_with(1)

    @patch.object(api, "user_service")
    def test_create_user_returns_user_on_success(self, mock_user_service):
        mock_user_service.create_user = AsyncMock(return_value=MOCK_USER)

        test_body = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2022-05-06"
        })

        response = client.post("/users", data=test_body)

        assert response.status_code == 201
        assert response.json() == json.loads(MOCK_USER.json())

        mock_user_service.create_user.assert_called_once()
