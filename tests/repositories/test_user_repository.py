import datetime
from unittest.mock import patch, AsyncMock, ANY

import pytest

from app.domain import User, Page, NEXT_PAGE_PREFIX, PageRequest
from app.repositories import UserRepository, DatabaseParseException, DatabaseException
from app.repositories.dtos import UserDTO
from tests.mock_data.mocks import MOCK_USER, MOCK_USER_PROTOTYPE, MOCK_EMPTY_PAGE
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

    # GET USERS
    @patch.object(user_repository, "pagination_query")
    async def test_get_users_calls_pagination_query_with_valid_params_on_page_request_without_cursor(self,
                                                                                                     pagination_query_fn_mock):
        pagination_query_fn_mock.side_effect = AsyncMock(return_value=MOCK_EMPTY_PAGE)

        page_request = PageRequest(cursor=None, size=5)

        res = await user_repository.get_users_paginated(page_request)

        assert len(res.data) == 0
        pagination_query_fn_mock.assert_called_once_with(
            query=ANY,
            order_column=UserDTO.c.id,
            order_column_value=None,
            object_order_attribute_name='id',
            page_request=page_request,
            row_mapping_fn=ANY
        )

    @patch.object(user_repository, "pagination_query")
    async def test_get_users_calls_pagination_query_with_valid_params_on_page_request_with_valid_cursor(self,
                                                                                                     pagination_query_fn_mock):
        pagination_query_fn_mock.side_effect = AsyncMock(return_value=MOCK_EMPTY_PAGE)

        page_request = PageRequest(cursor=NEXT_PAGE_PREFIX + "1", size=5)

        res = await user_repository.get_users_paginated(page_request)

        assert len(res.data) == 0
        pagination_query_fn_mock.assert_called_once_with(
            query=ANY,
            order_column=UserDTO.c.id,
            order_column_value=1,
            object_order_attribute_name='id',
            page_request=page_request,
            row_mapping_fn=ANY
        )
