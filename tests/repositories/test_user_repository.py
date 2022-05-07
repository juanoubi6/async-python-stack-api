import datetime
from unittest.mock import patch, AsyncMock

import pytest

from app.domain import User
from app.repositories import UserRepository, DatabaseParseException, DatabaseException
from tests.mock_data.mocks import MOCK_USER, MOCK_USER_PROTOTYPE
from tests.repositories.expected_queries import GET_USER_EXPECTED_QUERY, CREATE_USER_EXPECTED_QUERY

user_repository = UserRepository(db=AsyncMock())


@pytest.mark.asyncio
class TestUserRepository:

    # GET USER
    @patch.object(user_repository, "db")
    async def test_get_user_executes_valid_query(self, mock_db):
        mock_db.fetch_one = AsyncMock(return_value=None)

        await user_repository.get_user(1)

        query = mock_db.fetch_one.call_args[0][0]
        assert str(query) == GET_USER_EXPECTED_QUERY

    @patch.object(user_repository, "db")
    async def test_get_user_returns_user_on_success(self, mock_db):
        mock_db.fetch_one = AsyncMock(return_value={
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date.today()
        })

        response = await user_repository.get_user(1)

        assert isinstance(response, User)
        assert response == MOCK_USER

        mock_db.fetch_one.assert_called_once()

    @patch.object(user_repository, "db")
    async def test_get_user_returns_None_when_user_cannot_be_found(self, mock_db):
        mock_db.fetch_one = AsyncMock(return_value=None)

        response = await user_repository.get_user(1)

        assert response is None

        mock_db.fetch_one.assert_called_once()

    @patch.object(user_repository, "db")
    async def test_get_user_returns_DatabaseParseException_if_user_dto_cannot_be_parsed(self, mock_db):
        mock_db.fetch_one = AsyncMock(return_value={
            "id": 1,
            "first_name": None,
            "last_name": "Doe",
            "birth_date": datetime.date.today()
        })

        with pytest.raises(DatabaseParseException):
            await user_repository.get_user(1)

    @patch.object(user_repository, "db")
    async def test_get_user_returns_DatabaseException_on_db_error(self, mock_db):
        mock_db.fetch_one = AsyncMock(side_effect=Exception("error"))

        with pytest.raises(DatabaseException):
            await user_repository.get_user(1)

    # CREATE USER
    @patch.object(user_repository, "db")
    async def test_create_user_executes_valid_query(self, mock_db):
        mock_db.execute = AsyncMock(return_value=1)

        await user_repository.create_user(MOCK_USER_PROTOTYPE)

        query = mock_db.execute.call_args[0][0]
        assert str(query) == CREATE_USER_EXPECTED_QUERY

    @patch.object(user_repository, "db")
    async def test_create_user_returns_user_on_success(self, mock_db):
        mock_db.execute = AsyncMock(return_value=1)

        response = await user_repository.create_user(MOCK_USER_PROTOTYPE)

        assert isinstance(response, User)
        assert response.id == 1

        mock_db.execute.assert_called_once()

    @patch.object(user_repository, "db")
    async def test_create_user_returns_DatabaseParseException_if_user_dto_cannot_be_parsed(self, mock_db):
        mock_db.execute = AsyncMock(return_value=None)

        with pytest.raises(DatabaseParseException):
            await user_repository.create_user(MOCK_USER_PROTOTYPE)

    @patch.object(user_repository, "db")
    async def test_create_user_returns_DatabaseException_on_db_error(self, mock_db):
        mock_db.execute = AsyncMock(side_effect=Exception("error"))

        with pytest.raises(DatabaseException):
            await user_repository.create_user(MOCK_USER_PROTOTYPE)