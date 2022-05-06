from databases import Database
from pydantic import ValidationError

from app.domain import User, UserPrototype
from app.repositories.dtos import UserDTO
from .base_transactional_dao import BaseTransactionalDAO
from .exceptions import DatabaseException, DatabaseParseException


class UserRepository(BaseTransactionalDAO):
    def __init__(self, db: Database):
        super().__init__(db)

    async def get_user(self, user_id: int) -> User:
        query = UserDTO.select().where(UserDTO.c.id == user_id)

        try:
            user_dto = await self.db.fetch_one(query)
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
