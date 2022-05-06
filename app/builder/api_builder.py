from typing import Any

from databases import Database
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .database_builder import build_database
from app.repositories import UserRepository
from app.services import UserService


class FastAPIWrapper(FastAPI):
    def __init__(self, user_service: UserService, **extra: Any):
        super().__init__(**extra)
        self.user_service = user_service


async def build_api() -> FastAPIWrapper:
    database = await build_database()

    user_service = _create_user_service(database)

    api = FastAPIWrapper(
        user_service=user_service,
        default_response_class=JSONResponse
    )

    return api


def _create_user_service(db: Database) -> UserService:
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    return user_service
