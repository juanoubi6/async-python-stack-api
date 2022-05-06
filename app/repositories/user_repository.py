import datetime

from databases import Database

from app.domain import User, UserPrototype
from app.repositories.dtos import UserDTO


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_user(self, user_id: int) -> User:
        query = UserDTO.select().where(UserDTO.c.id == user_id)
        user_dto = await self.db.fetch_one(query)

        return User(
            id=user_dto.get("id"),
            first_name=user_dto.get("first_name"),
            last_name=user_dto.get("last_name"),
            birth_date=user_dto.get("birth_date")
        )

    async def create_user(self, prototype: UserPrototype) -> User:
        query = UserDTO.insert().values(
            first_name=prototype.first_name,
            last_name=prototype.last_name,
            birth_date=prototype.birth_date
        )

        inserted_id = await self.db.execute(query)

        return User(
            id=inserted_id,
            first_name=prototype.first_name,
            last_name=prototype.last_name,
            birth_date=prototype.birth_date
        )
