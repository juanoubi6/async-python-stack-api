from typing import Optional

from databases import Database
from pydantic import ValidationError
from sqlalchemy import asc, desc

from app.domain import User, UserPrototype, Page, PageRequest
from app.repositories.dtos import UserDTO
from .base_transactional_dao import BaseTransactionalDAO
from .exceptions import DatabaseException, DatabaseParseException
from .pagination import calculate_next_page_value, calculate_previous_page_value, calculate_data


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
    async def get_users(self, page_request: PageRequest) -> Page[User]:
        query = UserDTO.select()

        if page_request.is_next_cursor():
            query = query.where(UserDTO.c.id > int(page_request.get_cursor_value())).order_by(asc(UserDTO.c.id)).limit(
                page_request.size + 1)
        elif page_request.is_previous_cursor():
            query = query.where(UserDTO.c.id < int(page_request.get_cursor_value())).order_by(desc(UserDTO.c.id)).limit(
                page_request.size + 1)
        else:
            query = query.order_by(asc(UserDTO.c.id)).limit(page_request.size + 1)

        data = []
        try:
            rows = await self.db.fetch_all(query)
            for row in rows:
                data.append(User(
                    id=row.get("id"),
                    first_name=row.get("first_name"),
                    last_name=row.get("last_name"),
                    birth_date=row.get("birth_date")
                ))
        except ValidationError as vex:
            raise DatabaseParseException(str(vex))
        except Exception as ex:
            raise DatabaseException(str(ex))

        data.sort(key=lambda user: user.id)
        data_size = len(data)

        return_data = calculate_data(page_request, data)
        id_list = [str(user.id) for user in return_data]

        return Page(
            data=return_data,
            next_page=calculate_next_page_value(page_request, id_list, data_size),
            previous_page=calculate_previous_page_value(page_request, id_list, data_size)
        )
