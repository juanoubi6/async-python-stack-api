from typing import Optional, Callable, Mapping

from databases import Database
from pydantic import ValidationError

from app.domain import User, UserPrototype, Page, PageRequest
from app.repositories.dtos import UserDTO
from .base_transactional_dao import BaseTransactionalDAO
from .exceptions import DatabaseException, DatabaseParseException


class UserRepository(BaseTransactionalDAO):
    def __init__(self, db: Database):
        super().__init__(db)

    async def get_user(self, user_id: int) -> Optional[User]:
        query = UserDTO.select().where(UserDTO.c.id == user_id)

        try:
            user_dto = await self.db.fetch_one(query)
            if user_dto is None:
                return None

            user = User(
                id=user_dto.get("id"),
                first_name=user_dto.get("first_name"),
                last_name=user_dto.get("last_name"),
                birth_date=user_dto.get("birth_date")
            )
        except ValidationError as vex:
            raise DatabaseParseException(str(vex))
        except Exception as ex:
            raise DatabaseException(str(ex))

        return user

    async def create_user(self, prototype: UserPrototype) -> User:
        query = UserDTO.insert().values(
            first_name=prototype.first_name,
            last_name=prototype.last_name,
            birth_date=prototype.birth_date
        )

        try:
            inserted_id = await self.db.execute(query)

            user = User(
                id=inserted_id,
                first_name=prototype.first_name,
                last_name=prototype.last_name,
                birth_date=prototype.birth_date
            )
        except ValidationError as vex:
            raise DatabaseParseException(str(vex))
        except Exception as ex:
            raise DatabaseException(str(ex))

        return user

    # Users are sorted by id. They could be ordered by any other unique and sequential field
    async def get_users_paginated(self, page_request: PageRequest) -> Page[User]:
        base_query = UserDTO.select().limit(page_request.size + 1)
        order_column = UserDTO.c.id
        order_column_value = int(page_request.get_cursor_value()) if page_request.cursor is not None else None
        object_order_attribute_name = 'id'
        row_mapping_fn: Callable[[Mapping], User] = lambda row: User(
            id=row.get("id"),
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            birth_date=row.get("birth_date")
        )

        return await self.pagination_query(
            query=base_query,
            order_column=order_column,
            order_column_value=order_column_value,
            object_order_attribute_name=object_order_attribute_name,
            page_request=page_request,
            row_mapping_fn=row_mapping_fn
        )
