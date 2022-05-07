from fastapi import status

from app.domain import User, UserPrototype
from .api_wrapper import FastAPIWrapper
from .exception_handlers import ErrorResponse


def add_routes(wrapper: FastAPIWrapper):
    @wrapper.get(
        path="/users/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=User,
        responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}}
    )
    async def get_user(user_id: int):
        return await wrapper.user_service.get_user(user_id)

    @wrapper.post(
        path="/users",
        status_code=status.HTTP_201_CREATED,
        response_model=User
    )
    async def create_user(prototype: UserPrototype):
        return await wrapper.user_service.create_user(prototype)
