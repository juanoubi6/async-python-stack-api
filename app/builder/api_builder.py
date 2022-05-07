from databases import Database

from app.http import FastAPIWrapper
from app.repositories import UserRepository
from app.services import UserService
from .database_builder import build_database


def _create_user_service(db: Database) -> UserService:
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    return user_service


def add_events(wrapper: FastAPIWrapper):
    @wrapper.on_event("startup")
    async def add_runtime_objects():
        database = await build_database(wrapper.config.db_config)
        user_service = _create_user_service(database)

        wrapper.user_service = user_service
