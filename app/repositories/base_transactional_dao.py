from typing import Any, List, TypeVar, Callable, Mapping

from databases import Database
from databases.core import Transaction
from pydantic import ValidationError
from sqlalchemy import asc, desc

from .exceptions import TransactionAlreadyStartedException, DatabaseParseException, DatabaseException
from ..domain import Page, PageRequest, NEXT_PAGE_PREFIX, PREVIOUS_PAGE_PREFIX

T = TypeVar('T')

class BaseTransactionalDAO:
    def __init__(self, db: Database, tx: Transaction = None):
        self.db = db
        self.tx = tx

    async def start_tx(self):
        if self.tx is not None:
            raise TransactionAlreadyStartedException("Transaction already started")

        self.tx = await self.db.transaction()

    async def commit_tx(self):
        if self.tx is None:
            return

        await self.tx.commit()
        self.tx = None

    async def rollback_tx(self):
        if self.tx is None:
            return

        await self.tx.rollback()
        self.tx = None

    async def pagination_query(
            self, query, order_column, order_column_cursor_value,object_order_attribute_name:str, page_request: PageRequest, row_mapping_fn: Callable[[Mapping], T]
    ) -> Page[T]:
        if page_request.is_next_cursor():
            query = query.where(order_column > order_column_cursor_value).order_by(asc(order_column)).limit(
                page_request.size + 1)
        elif page_request.is_previous_cursor():
            query = query.where(order_column < order_column_cursor_value).order_by(desc(order_column)).limit(
                page_request.size + 1)
        else:
            query = query.order_by(asc(order_column)).limit(page_request.size + 1)

        try:
            rows = await self.db.fetch_all(query)
            data = [row_mapping_fn(row) for row in rows]
        except ValidationError as vex:
            raise DatabaseParseException(str(vex))
        except Exception as ex:
            raise DatabaseException(str(ex))

        data.sort(key=lambda elem: getattr(elem, object_order_attribute_name))
        data_size = len(data)

        return_data = _calculate_data(page_request, data)
        id_list = [str(getattr(elem, object_order_attribute_name)) for elem in return_data]

        return Page(
            data=return_data,
            next_page=_calculate_next_page(page_request, id_list, data_size),
            previous_page=_calculate_previous_page(page_request, id_list, data_size)
        )


def _calculate_data(page_request: PageRequest, data: List[Any]) -> List[Any]:
    if len(data) > page_request.size:
        if page_request.is_previous_cursor():
            return data[1:]
        if page_request.is_next_cursor() or page_request.cursor is None:
            return data[:-1]

    return data


def _calculate_next_page(page_request: PageRequest, data_ids: List[str], data_size: int) -> str | None:
    if page_request.is_previous_cursor() or data_size > page_request.size:
        return NEXT_PAGE_PREFIX + data_ids[len(data_ids) - 1]

    return None


def _calculate_previous_page(page_request: PageRequest, data_ids: List[str], data_size: int) -> str | None:
    if page_request.cursor is None:
        return None

    if page_request.is_next_cursor() or data_size > page_request.size:
        return PREVIOUS_PAGE_PREFIX + data_ids[0]

    return None
