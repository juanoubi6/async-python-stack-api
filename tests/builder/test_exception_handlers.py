import unittest
from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient

from app import api
from app.domain import ResourceNotFoundException, DomainException
from app.repositories import DatabaseException, DatabaseParseException

client = TestClient(api)


class TestExceptionHandlers(unittest.TestCase):

    @patch.object(api, "user_service")
    def test_when_DatabaseException_is_thrown_then_api_returns_400(self, mock_user_service):
        err_message = "some error"
        mock_user_service.get_user = AsyncMock(side_effect=DatabaseException(err_message))

        response = client.get("/users/1")

        assert response.status_code == 400
        assert response.json()["error"] == err_message

    @patch.object(api, "user_service")
    def test_when_DatabaseParseException_is_thrown_then_api_returns_400(self, mock_user_service):
        err_message = "some error"
        mock_user_service.get_user = AsyncMock(side_effect=DatabaseParseException(err_message))

        response = client.get("/users/1")

        assert response.status_code == 400
        assert response.json()["error"] == err_message

    @patch.object(api, "user_service")
    def test_when_ResourceNotFoundException_is_thrown_then_api_returns_400(self, mock_user_service):
        err_message = "some error"
        mock_user_service.get_user = AsyncMock(side_effect=ResourceNotFoundException(err_message))

        response = client.get("/users/1")

        assert response.status_code == 404
        assert response.json()["error"] == err_message

    @patch.object(api, "user_service")
    def test_when_DomainException_is_thrown_then_api_returns_400(self, mock_user_service):
        err_message = "some error"
        mock_user_service.get_user = AsyncMock(side_effect=DomainException(err_message))

        response = client.get("/users/1")

        assert response.status_code == 400
        assert response.json()["error"] == err_message
