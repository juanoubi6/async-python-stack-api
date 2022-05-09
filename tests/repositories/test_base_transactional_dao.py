from typing import Callable, Mapping
from unittest.mock import patch, AsyncMock

import pytest

from app.domain import User, PageRequest, NEXT_PAGE_PREFIX, PREVIOUS_PAGE_PREFIX
from app.repositories.base_transactional_dao import BaseTransactionalDAO
from app.repositories.dtos import UserDTO
from tests.mock_data.mocks import create_mock_user_dto

base_dao = BaseTransactionalDAO(db=AsyncMock())

base_query = UserDTO.select()
order_column = UserDTO.c.id
object_order_attribute_name = 'id'
row_mapping_fn: Callable[[Mapping], User] = lambda row: User(
    id=row.get("id"),
    first_name=row.get("first_name"),
    last_name=row.get("last_name"),
    birth_date=row.get("birth_date")
)

@pytest.mark.asyncio
class TestBaseTransactionalDAORepository:

    @patch.object(base_dao, "db")
    async def test_pagination_query_without_cursor_and_more_retrieved_records_than_page_size(self, mock_db):
        page_request = PageRequest(cursor=None, size=5)

        mock_db.fetch_all = AsyncMock(return_value=[
            create_mock_user_dto(1), create_mock_user_dto(2), create_mock_user_dto(3),
            create_mock_user_dto(4), create_mock_user_dto(5), create_mock_user_dto(6)
        ])

        result = await base_dao.pagination_query(
            query=base_query,
            order_column=order_column,
            order_column_value=None,
            object_order_attribute_name=object_order_attribute_name,
            page_request=page_request,
            row_mapping_fn=row_mapping_fn
        )

        assert len(result.data) == 5
        assert result.next_page == NEXT_PAGE_PREFIX + '5'
        assert result.previous_page is None

    @patch.object(base_dao, "db")
    async def test_pagination_query_with_next_cursor_and_more_retrieved_records_than_page_size(self, mock_db):
        page_request = PageRequest(cursor=NEXT_PAGE_PREFIX + '5', size=5)

        mock_db.fetch_all = AsyncMock(return_value=[
            create_mock_user_dto(6), create_mock_user_dto(7), create_mock_user_dto(8),
            create_mock_user_dto(9), create_mock_user_dto(10), create_mock_user_dto(11)
        ])

        result = await base_dao.pagination_query(
            query=base_query,
            order_column=order_column,
            order_column_value=int(page_request.get_cursor_value()),
            object_order_attribute_name=object_order_attribute_name,
            page_request=page_request,
            row_mapping_fn=row_mapping_fn
        )

        assert len(result.data) == 5
        assert result.next_page == NEXT_PAGE_PREFIX + '10'
        assert result.previous_page == PREVIOUS_PAGE_PREFIX + '6'

    @patch.object(base_dao, "db")
    async def test_pagination_query_with_next_cursor_and_less_retrieved_records_than_page_size(self, mock_db):
        page_request = PageRequest(cursor=NEXT_PAGE_PREFIX + '10', size=5)

        mock_db.fetch_all = AsyncMock(return_value=[
            create_mock_user_dto(11), create_mock_user_dto(12), create_mock_user_dto(13),
        ])

        result = await base_dao.pagination_query(
            query=base_query,
            order_column=order_column,
            order_column_value=int(page_request.get_cursor_value()),
            object_order_attribute_name=object_order_attribute_name,
            page_request=page_request,
            row_mapping_fn=row_mapping_fn
        )

        assert len(result.data) == 3
        assert result.next_page is None
        assert result.previous_page == PREVIOUS_PAGE_PREFIX + '11'

    @patch.object(base_dao, "db")
    async def test_pagination_query_with_previous_cursor_and_more_retrieved_records_than_page_size(self, mock_db):
        page_request = PageRequest(cursor=PREVIOUS_PAGE_PREFIX + '11', size=5)

        mock_db.fetch_all = AsyncMock(return_value=[
            create_mock_user_dto(5), create_mock_user_dto(6), create_mock_user_dto(7),
            create_mock_user_dto(8), create_mock_user_dto(9), create_mock_user_dto(10)
        ])

        result = await base_dao.pagination_query(
            query=base_query,
            order_column=order_column,
            order_column_value=int(page_request.get_cursor_value()),
            object_order_attribute_name=object_order_attribute_name,
            page_request=page_request,
            row_mapping_fn=row_mapping_fn
        )

        assert len(result.data) == 5
        assert result.next_page == NEXT_PAGE_PREFIX + '10'
        assert result.previous_page == PREVIOUS_PAGE_PREFIX + '6'

    @patch.object(base_dao, "db")
    async def test_pagination_query_with_previous_cursor_and_less_retrieved_records_than_page_size(self, mock_db):
        page_request = PageRequest(cursor=PREVIOUS_PAGE_PREFIX + '6', size=5)

        mock_db.fetch_all = AsyncMock(return_value=[
            create_mock_user_dto(1), create_mock_user_dto(2), create_mock_user_dto(3),
            create_mock_user_dto(4), create_mock_user_dto(5)
        ])

        result = await base_dao.pagination_query(
            query=base_query,
            order_column=order_column,
            order_column_value=int(page_request.get_cursor_value()),
            object_order_attribute_name=object_order_attribute_name,
            page_request=page_request,
            row_mapping_fn=row_mapping_fn
        )

        assert len(result.data) == 5
        assert result.next_page == NEXT_PAGE_PREFIX + '5'
        assert result.previous_page is None
