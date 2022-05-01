from typing import Any

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.repositories import UserRepository
from app.services import UserService


class FastAPIWrapper(FastAPI):
    def __init__(self, user_service: UserService, **extra: Any):
        super().__init__(**extra)
        self.user_service = user_service


def build_api() -> FastAPIWrapper:
    user_service = _create_user_service()

    api = FastAPIWrapper(
        user_service=user_service,
        default_response_class=JSONResponse
    )

    return api


def _create_user_service() -> UserService:
    user_repository = UserRepository("db")
    user_service = UserService(user_repository)

    return user_service
