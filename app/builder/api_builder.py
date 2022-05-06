import os
from typing import Any

from databases import Database
from fastapi import FastAPI

from app.config import get_config, AppConfig
from app.repositories import UserRepository
from app.services import UserService
from .database_builder import build_database
from .exception_handlers import add_error_handlers


class FastAPIWrapper(FastAPI):
    def __init__(self, user_service: UserService = None, config: AppConfig = None, **extra: Any):
        super().__init__(**extra)
        add_error_handlers(self)
        self.config = config if config is not None else get_config(os.getenv("ENV", "local"))
        self.user_service = user_service


async def decorate_api(api: FastAPIWrapper):
    database = await build_database(api.config.db_config)
    user_service = _create_user_service(database)

    api.user_service = user_service


def _create_user_service(db: Database) -> UserService:
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    return user_service
