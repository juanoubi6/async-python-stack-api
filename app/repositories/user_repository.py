import datetime

from databases import Database

from app.domain import User, UserPrototype
from app.repositories.dtos import UserDTO


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_user(self, user_id: int) -> User:
        statement = UserDTO.select()
        res1 = await self.db.fetch_one("select * from users")
        return User(
            id=user_id, first_name="John", last_name="Doe", birth_date=datetime.date.today()
        )

    async def create_user(self, prototype: UserPrototype) -> User:
        #Some insert logic
        return User(
            id=1, first_name=prototype.first_name, last_name=prototype.last_name, birth_date=prototype.birth_date
        )
