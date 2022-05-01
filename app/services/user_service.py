from app.domain import User, UserPrototype
from app.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> User:
        return await self.user_repository.get_user(user_id)

    async def create_user(self, prototype: UserPrototype) -> User:
        return await self.user_repository.create_user(prototype)
