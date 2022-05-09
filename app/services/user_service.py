from app.domain import User, UserPrototype, ResourceNotFoundException, Page, PageRequest
from app.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repository.get_user(user_id)
        if user is None:
            raise ResourceNotFoundException("User could not be found")

        return user

    async def get_users_paginated(self, page_request: PageRequest) -> Page[User]:
        return await self.user_repository.get_users_paginated(page_request)

    async def create_user(self, prototype: UserPrototype) -> User:
        # Suppose we have a lot of business logic here, and if something fails we need to roll back
        # any operation made at repository level.
        try:
            await self.user_repository.start_tx()
            # Some business logic
            user = await self.user_repository.create_user(prototype)
            # Some more business logic
        except Exception as ex:
            await self.user_repository.rollback_tx()
            raise ex
        else:
            await self.user_repository.commit_tx()

        return user
